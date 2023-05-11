from flask import Flask, jsonify, send_from_directory, Response
import os
import json
from flask_cors import CORS
import cv2
import time
import threading
from itertools import count

gen_frames_id_generator = count()
max_gen_frames = 4
num_gen_frames = 0
gen_frames_counter = 0
gen_frames_condition = threading.Condition()
image_folder = './raw/2011_09_26_drive_0113_extract/image_03/data'
result_path = './results/2011_09_26_drive_0113_extract.json'
safe_img_path = './raw/signs/safe.png'
danger_img_path = './raw/signs/danger.png'

app = Flask(__name__)
CORS(app)

@app.route('/raw/<path:path>')
def send_report(path):
    return send_from_directory('raw', path)

@app.route('/')
def get_jsons():
    jsons_folder = './jsons'
    json_files = [f for f in os.listdir(jsons_folder) if f.endswith('.json')]
    return jsonify(json_files)

@app.route('/frame/<file>/<time>')
def get_frame(file, time):
    jsons_folder = './jsons'
    json_file_path = os.path.join(jsons_folder, file)
    if not os.path.isfile(json_file_path):
        return jsonify({'error': 'No such JSON file.'}), 404
    with open(json_file_path) as f:
        try:
            data = json.load(f)
            value = data[time]
        except (KeyError, json.JSONDecodeError):
            return jsonify({'error': 'No such time in this JSON file.'}), 404
    return jsonify(value)

@app.route('/results')
def get_all_results():
    jsons_folder = './results'
    json_files = [f for f in os.listdir(jsons_folder) if f.endswith('.json')]
    return jsonify(json_files)

@app.route('/results/<file>')
def get_result(file):
    jsons_folder = './results'
    json_file_path = os.path.join(jsons_folder, file)
    if not os.path.isfile(json_file_path):
        return jsonify({'error': 'No such JSON file.'}), 404
    with open(json_file_path) as f:
        data = json.load(f)
        return jsonify(data)

@app.route('/video_feed/<path>')
def video_feed(path):
    global max_gen_frames
    global num_gen_frames

    # Check if we have too many video feeds
    if num_gen_frames >= max_gen_frames:
        return jsonify({'error': 'Too many video feeds.'}), 429
    else:
        gen_frames_id = next(gen_frames_id_generator)
        num_gen_frames += 1

        if path != 'results':
            return Response(gen_frames(path, gen_frames_id), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response(gen_results(path, gen_frames_id), mimetype='multipart/x-mixed-replace; boundary=frame')

# This function is used to generate frames for the video feed        
def gen_frames( path, gen_frames_id ):
    global gen_frames_counter
    global num_gen_frames
    global image_folder

    image_folder_path = os.path.join(image_folder, path)

    frame_rate = 30  # Adjust this value to control the frame rate of the video feed
    proper_wait_time = 1 / frame_rate

    img_files = sorted(os.listdir(image_folder_path))
    num_files = len(img_files)
    i = 0

    while True:
        start_time = time.time()
        img_path = os.path.join(image_folder_path, img_files[i%num_files])
        i += 1

        frame = cv2.imread(img_path)
        if frame is None:
            continue

        with gen_frames_condition:
            while gen_frames_counter % num_gen_frames != gen_frames_id:
                gen_frames_condition.wait()  # Wait for our turn

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            gen_frames_counter += 1
            gen_frames_condition.notify_all()  # Notify all waiting gen_frames functions

        end_time = time.time()
        if end_time - start_time < proper_wait_time:
            time.sleep(proper_wait_time - (end_time - start_time))

# This function is used to generate Result frames for a video feed
def gen_results(path, gen_frames_id ):
    global gen_frames_counter
    global num_gen_frames
    frame_rate = 30  # Adjust this value to control the frame rate of the video feed
    proper_wait_time = 1 / frame_rate
    safe_image = cv2.imread(safe_img_path)
    danger_image = cv2.imread(danger_img_path)

    with open(result_path) as json_file:
        data = json.load(json_file)

    i = 0

    while True:

        i = i % len(data)
        start_time = time.time()

        with gen_frames_condition:
            while gen_frames_counter % num_gen_frames != gen_frames_id:
                gen_frames_condition.wait()  # Wait for our turn

            key = f"{i:010}"
            if key in data:
                is_safe = data[key]
                frame = safe_image if is_safe else danger_image
                ret, buffer = cv2.imencode('.png', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
            else:
                i = 0
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            gen_frames_counter += 1
            gen_frames_condition.notify_all()  # Notify all waiting gen_frames functions

        end_time = time.time()
        if end_time - start_time < proper_wait_time:
            time.sleep(proper_wait_time - (end_time - start_time))
        i += 1

if __name__ == '__main__':
    app.run(debug=True)