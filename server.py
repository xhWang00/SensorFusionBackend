from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

@app.route('/raw')
def send_raw():
    return app.send_static_file('raw')

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

if __name__ == '__main__':
    app.run()