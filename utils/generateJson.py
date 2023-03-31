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

check_white_pixels('raw/2011_09_26_drive_0048_extract/image_03/data/edges', 32000)