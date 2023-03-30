import cv2
import numpy as np
import os

def detect_edges(input_folder, output_folder):
    # Loop through all subdirectories (i.e., video frame directories) in the input folder
    for subfolder in os.listdir(input_folder):
        if os.path.isdir(os.path.join(input_folder, subfolder)):
            # Create a corresponding subdirectory in the output folder
            output_subfolder = os.path.join(output_folder, subfolder)
            os.makedirs(output_subfolder, exist_ok=True)
            # Loop through all files (i.e., frames) in the subdirectory
            for filename in os.listdir(os.path.join(input_folder, subfolder)):
                # Check if the file is an image
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    # Read the image file
                    img = cv2.imread(os.path.join(input_folder, subfolder, filename))
                    # Convert the image to grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Detect edges using the Canny edge detection algorithm
                    edges = cv2.Canny(gray, 100, 200)
                    # Save the edges image to the output subdirectory
                    output_filename = os.path.join(output_subfolder, filename)
                    cv2.imwrite(output_filename, edges)