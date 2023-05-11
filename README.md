# Sensor Fusion Lane Merging Safety Project - Backend
Backend for Mathworks (Sensor Fusion for Autonomous Systems) project.

This repository hosts the backend for the Sensor Fusion Lane Merging Safety Project. It uses Flask, a Python web framework, to serve the output of our sensor fusion algorithm, the data and video frames, to the front end.

## Project Overview

This backend server is designed to send information to the frontend about the lane merging safety. The data sent includes the output of the sensor fusion algorithm, raw data, and video frames. The server also provides an interface to view results and video feeds.

## Installation

To run this project, you will need Python 3.6 or above, and to install the required dependencies, you can use pip:

```bash
pip install requirements.txt
```

Usage
Once you've installed the necessary packages, you can start the server by running the server.py script:

```
python server.py
```

This will start the Flask server on your machine. By default, Flask runs on port 5000, so you can visit localhost:5000 in your browser to interact with the server.

The backend provides the following API endpoints:

GET /raw/<path:path> - Serves raw data files from the specified path.
GET / - Returns a list of all JSON files in the server.
GET /frame/<file>/<time> - Returns a specific frame from a file at a given time.
GET /results - Returns a list of all result JSON files.
GET /results/<file> - Returns a specific result file.
GET /video_feed/<path> - Returns a video feed for the provided path.
