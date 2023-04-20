import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# Load KITTI dataset
basedir = './raw'
date = '2011_09_26'
drive = '0048'

def load_velodyne_points(frame, base_dir, date, drive):
    file_path = os.path.join(base_dir, date + '_drive_' + drive + '_extract', 'velodyne_points', 'data', f'{frame:010d}.txt')
    points = np.loadtxt(file_path, dtype=np.float32)
    return points


def plot_sensor_detection(velodyne_points,frame_number, output_dir):
    # Filter points based on z-values
    filtered_points = velodyne_points[(velodyne_points[:, 2] >= 0.01) & (velodyne_points[:, 2] <= 2)]

    x = filtered_points[:, 0]
    y = filtered_points[:, 1]
    z = filtered_points[:, 2]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title('Sensor Detections')
    ax.set_aspect('equal')

    # Set dark theme background
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')

    # Plot the car (a rectangle with rounded edges at the origin)
    car_color = '#4474e3'  # Set the color to the specified RGB values
    car = FancyBboxPatch((0, 0), 4, 6, boxstyle="round,pad=1", fc=car_color, label='Car')
    ax.add_patch(car)

    # Plot the lidar points (top-down view)
    ax.scatter(y, x, c='#c9270e', s=0.5, label='Lidar points')

    # Shrink the plot range and vision cone by a factor of 0.5
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)

    # Save the plot as a JPEG
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f'frame_{frame_number:04d}.jpg')
    plt.savefig(output_path, format='jpeg', dpi=300, bbox_inches='tight')

def process_all_frames(input_dir='./raw/2011_09_26_drive_0048_extract/velodyne_points/data', 
                       output_dir='./raw/2011_09_26_drive_0048_extract/image_03/data/plot'):
    
    frame_files = sorted(os.listdir(input_dir))

    for idx, file in enumerate(frame_files):
        if file.endswith('.txt'):
            velodyne_points = load_velodyne_points(idx, basedir, date, drive)
            plot_sensor_detection(velodyne_points, idx, output_dir)
            print(f"Processed frame {idx}")


process_all_frames()
# frame_number = 0  # Choose the frame number
# while frame_number < 1:
#     velodyne_points = load_velodyne_points(frame_number, basedir, date, drive)
#     plot_sensor_detection(velodyne_points)
#     frame_number += 1
