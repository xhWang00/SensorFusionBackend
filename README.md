# SensorFusionBackend
Backend for Mathworks (Sensor Fusion for Autonomous Systems) project.

## File sturcture

| File/Folder | Description |
| --- | --- | 
| `demo/` | Demostration functions
| `jsons/` | Results from each algorithm, semi-finished and to be combined by `algorithm_fusion.ipynb |
| `raw/` | Raw data from [Kitti](https://www.cvlibs.net/datasets/kitti/raw_data.php)
| `results/` | Final returns from  MLPClassifier|
| `utils/` | Algorithms, labeled dataset, and `cars.xml` for [Cascade Classifier](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) |
| `algorithm_fusion.ipynb` | MLPClassifier to fuse results from [Cascade Classifier](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) and many other algorithms
| `labeling_ins.md` | Labeling insturciton
| `model.pkl` | Trained MLPClassifier model ready to inference
| `server.py` | Sample flask back-end web server

## Usage

### 1. Create and start virtual environment, and install dependencies

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

### 2. Prepare the dataset

Download any `[unsynced+unrectified data]` from [Kitti](https://www.cvlibs.net/datasets/kitti/raw_data.php), unzip them to `/raw` and make sure it has the following structure:
```
/raw
    /<dataset 1>
        /image03
            /data
                ...
        /velodyne_points
            /data
                ...
    /<dataset 2>
        /image03
            /data
                ...
        /velodyne_points
            /data
                ...
    ...
```

### 3. Run the algorithms

```bash
$ python3 utils/generateJson.py
```

This shall generate simi-finished algorithm result json files for each dataset under `jsons`.

### 4. Fuse the results

```bash
$ jupyter notebook
```

And modify as needed, it shall be straightforward.

### 5. Run the back-end web server

```bash
$ python3 server.py
```