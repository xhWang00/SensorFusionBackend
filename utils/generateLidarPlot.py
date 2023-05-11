import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# Load KITTI dataset
basedir = './raw'
date = '2011_09_26'
drive = '0113'

# function to load velodyne points
# frame: frame number
# base_dir: base directory of dataset
# date: date of dataset
# drive: drive number
# returns: velodyne points for the given frame
def load_velodyne_points(frame, base_dir, date, drive):
    file_path = os.path.join(base_dir, date + '_drive_' + drive + '_extract', 'velodyne_points', 'data', f'{frame:010d}.txt')
    points = np.loadtxt(file_path, dtype=np.float32)
    return points

# function to plot sensor detection
# velodyne_points: velodyne points for the given frame
# frame_number: frame number
# output_dir: output directory to save the plot
# Saves the plots as a JPEGs
def plot_sensor_detection(velodyne_points,frame_number, output_dir):
    # Filter points based on z-values
    filtered_points = velodyne_points[(velodyne_points[:, 2] >= -1.4) & (velodyne_points[:, 2] <= 2)]

    x = filtered_points[:, 0]
    y = filtered_points[:, 1]
    z = filtered_points[:, 2]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title('Sensor Detections')
    ax.set_aspect('equal')

    # Set dark theme background
    fig.patch.set_facecolor('#222222')
    ax.set_facecolor('#222222')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')

    # Plot the car (a rectangle with rounded edges at the origin)
    car_color = '#17cc20'  # Set the color to the specified RGB values
    car = FancyBboxPatch((-0.5, -0.5), 0.9, 1.88, boxstyle="round,pad=0.4", fc=car_color, label='Car')
    ax.add_patch(car)

    # Plot the lidar points (top-down view)
    ax.scatter(-y, x, c='#c9270e', s=(0.3), label='Lidar points')

    # Shrink the plot range and vision cone by a factor of 0.5
    ax.set_xlim(-17, 17)
    ax.set_ylim(-20, 20)

    # plt.show()
    # Save the plot as a JPEG
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f'frame_{frame_number:04d}.jpg')
    plt.savefig(output_path, format='jpeg', dpi=300, bbox_inches='tight')
    plt.close()

def process_all_frames(input_dir, output_dir):
    
    frame_files = sorted(os.listdir(input_dir))

    for idx, file in enumerate(frame_files):
        if file.endswith('.txt'):
            velodyne_points = load_velodyne_points(idx, basedir, date, drive)
            plot_sensor_detection(velodyne_points, idx, output_dir)
            print(f"Processed frame {idx}")

# function to plot sensor detection in 3D
def plot_sensor_detection_3d(velodyne_points):
    filtered_points = velodyne_points[(velodyne_points[:, 2] >= -1.45) & (velodyne_points[:, 2] <= 2)]


    x = filtered_points[:, 0]
    y = filtered_points[:, 1]
    z = filtered_points[:, 2]

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')

    # Set dark theme background
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.w_xaxis.line.set_color('white')
    ax.w_yaxis.line.set_color('white')
    ax.w_zaxis.line.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.tick_params(colors='white')

    ax.set_title('Sensor Detection')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Plot the LiDAR points (3D view)
    ax.scatter(x, y, z, c='green', s=0.5, label='LiDAR points')

    ax.legend()
    plt.show()



input_dir = os.path.join(basedir, date + '_drive_' + drive + '_extract', 'velodyne_points', 'data')
output_dir = os.path.join(basedir, date + '_drive_' + drive + '_extract', 'image_03', 'data', 'plot')
process_all_frames( input_dir, output_dir)
 