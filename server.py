from flask import Flask, jsonify, send_from_directory, Response, request
import os
import json
from flask_cors import CORS
import cv2
import time
import threading
from itertools import count

gen_frames_id_generator = count()
max_gen_frames = 3
num_gen_frames = 0
gen_frames_counter = 0
gen_frames_condition = threading.Condition()

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

@app.route('/video_feed/<path>')
def video_feed(path):
    global max_gen_frames
    global num_gen_frames

    print(num_gen_frames, max_gen_frames)
    if num_gen_frames >= max_gen_frames:

        return jsonify({'error': 'Too many video feeds.'}), 429
    else:
        gen_frames_id = next(gen_frames_id_generator)
        num_gen_frames += 1
        return Response(gen_frames(path, gen_frames_id), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames( edge, gen_frames_id ):
    global gen_frames_counter
    global num_gen_frames

    image_folder = './raw/2011_09_26_drive_0048_extract/image_03/data'
    image_folder_path = os.path.join(image_folder, edge)

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


if __name__ == '__main__':
    app.run(debug=True)