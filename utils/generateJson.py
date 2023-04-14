import os
import cv2
import json
import math

# Sweet point to be 1.5 and 32000.
MAGNITUDE_RANGE = 1.5
CV_RANGE = 32000

def detect_edges(input_folder):
    # Create the "edges" sub-folder if it doesn't already exist
    output_folder = os.path.join(input_folder, "edges")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Load the image and convert it to grayscale
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Canny edge detection
            edges = cv2.Canny(gray, 100, 200)

            # Save the edges image to the "edges" sub-folder
            edges_filename = os.path.join(output_folder, filename)
            cv2.imwrite(edges_filename, edges)
    
    print('[LOG] Edge images for ' + input_folder + ' generated.')


def check_magnitudes(input_folder, range_value):
    results = {}

    # Sort the txt files based on their filename
    filenames = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")], key=lambda x: int(os.path.splitext(x)[0]))

    for filename in filenames:
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Split the line into its four floating point numbers
                x, y, z, _ = map(float, line.strip().split())

                # Calculate the magnitude of the x, y, z coordinates
                magnitude = math.sqrt(x**2 + y**2 + z**2)

                # Compare the magnitude with the given range value
                if magnitude >= range_value:
                    continue

                # If any magnitude is less than the range value, set the result to False
                results[filename] = False
                break
            else:
                # All magnitudes in the file were greater than or equal to the range value
                results[filename] = True

    # Save the results dictionary to a JSON file in the input folder
    output_file = os.path.join(input_folder, "magnitude.json")
    with open(output_file, "w") as f:
        json.dump(results, f)

    print('[LOG] magnitudes.json for ' + input_folder + ' generated.')


def check_white_pixels(input_folder, range_value):
    results = {}

    # Get a list of all edge images in the input folder
    filenames = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")], key=lambda x: int(os.path.splitext(x)[0]))

    for filename in filenames:
        filepath = os.path.join(input_folder, filename)
        img = cv2.imread(filepath)

        # Count the number of white pixels in the image
        white_pixels = cv2.countNonZero(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

        # Compare the number of white pixels with the given range value
        if white_pixels > range_value:
            results[filename] = False
        else:
            results[filename] = True

    # Save the results dictionary to a JSON file in the input folder
    output_file = os.path.join(input_folder, "cv.json")
    with open(output_file, "w") as f:
        json.dump(results, f)

    print('[LOG] cv.json for ' + input_folder + ' generated.')


def detect_cars(image):
    # Load the Haar Cascade XML file for cars
    car_cascade = cv2.CascadeClassifier('./utils/cars.xml')

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect cars using the Haar Cascade
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Return the number of cars detected
    return len(cars)


def detect_cars_in_images(input_folder):
    result = {}

    for filename in os.listdir(input_folder):
        if  filename.endswith('.png'):
            # Load the image and get its dimensions
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            height, width, _ = image.shape

            # Crop the image into four equal parts
            top_left = image[0:height//2, 0:width//2]
            top_right = image[0:height//2, width//2:width]
            bottom_left = image[height//2:height, 0:width//2]
            bottom_right = image[height//2:height, width//2:width]

            # Use OpenCV to detect cars in the bottom-right and bottom-left parts
            bottom_left_cars = detect_cars(bottom_left)
            bottom_right_cars = detect_cars(bottom_right)

            # Save the results as a dictionary
            result[filename] = {"bottom_left": bottom_left_cars, "bottom_right": bottom_right_cars}

    # Save the result dictionary as a JSON file
    with open(os.path.join(input_folder, 'cars.json'), 'w') as outfile:
        json.dump(result, outfile)

    print('[LOG] cars.json for ' + input_folder + ' generated.')


def combine_json_files(input_folder, output_folder):
    # Get a list of all dataset folders in the input folder
    dataset_folders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]

    # Loop through each dataset folder and combine the cv.json and magnitude.json files
    for dataset_folder in dataset_folders:
        # Load the cv.json file
        cv_file_path = os.path.join(input_folder, dataset_folder, "image_03", "data", "edges", "cv.json")
        with open(cv_file_path, "r") as f:
            cv_data = json.load(f)

        # Load the magnitude.json file
        mag_file_path = os.path.join(input_folder, dataset_folder, "velodyne_points", "data", "magnitude.json")
        with open(mag_file_path, "r") as f:
            mag_data = json.load(f)

        # Load the cars.json file
        cars_file_path = os.path.join(input_folder, dataset_folder, "image_03", "data", "cars.json")
        with open(cars_file_path, "r") as f:
            cars_data = json.load(f)

        # Combine the two files, loop from cv since there will always be more video frames than velodyne_points.
        combined_data = {}
        for k in cv_data.keys():
            combined_key = k[:-4] # Remove .png from it.
            velodyne_key = combined_key + '.txt'
            if velodyne_key in mag_data:
                combined_data[combined_key] = {"edges": cv_data[k], "magnitude": mag_data[velodyne_key], "cascadeClassifier": cars_data[k]}
            else:
                combined_data[combined_key] = {"edges": cv_data[k], "magnitude": None, "cascadeClassifier": cars_data[k]}


        # Save the combined file to the output folder
        output_file_path = os.path.join(output_folder, dataset_folder + ".json")
        with open(output_file_path, "w") as f:
            json.dump(combined_data, f)


if __name__ == '__main__':
    dataset_folders = [f for f in os.listdir('./raw') if os.path.isdir(os.path.join('./raw', f))]

    for dataset in dataset_folders:
        detect_edges(os.path.join("raw", dataset, "image_03", "data"))
        check_magnitudes(os.path.join("raw", dataset, "velodyne_points", "data"), MAGNITUDE_RANGE)
        check_white_pixels(os.path.join("raw", dataset, "image_03", "data", "edges"), CV_RANGE)
        detect_cars_in_images(os.path.join("raw", dataset, "image_03", "data"))
    
    combine_json_files('./raw', './jsons')