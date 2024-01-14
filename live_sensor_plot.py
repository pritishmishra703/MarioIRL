"""
live_sensor_plot.py

This script collects sensor data from a connected device over a socket connection and displays a live plot of the 
sum of the x, y, and z values. The collected data is also printed periodically with the data speed.

Usage:
1. Make sure the required dependencies (numpy, matplotlib) are installed.
2. Update the HOST and PORT variables to match your socket configuration.
3. Run the script: `python live_sensor_plot.py`
"""

import re
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

HOST = '192.168.97.32'
PORT = 5000


def update_plot(sensor_data, line):
    """
    Update the plot with the latest data.

    Args:
        sensor_data (ndarray): Array containing sensor data.
        line (Line2D): Line object representing the plot.

    Returns:
        None
    """
    line.set_data(np.arange(len(sensor_data[-50:])), np.sum(sensor_data[-50:], axis=1))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()


# Initialize empty lists to store the data points
sensor_data = np.empty((0, 3), float)

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Sum of x, y, z')
ax.set_xlim(0, 50)
ax.set_ylim(-25, 25)
ax.set_xlabel('Time')
ax.set_ylabel('Sum of x, y, z')
ax.set_title('Live Plot of Sum of x, y, z')
ax.legend()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening for incoming connections on {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")

    # Compile regex patterns
    x_regex = re.compile(r'"x":"([^"]+)"')
    y_regex = re.compile(r'"y":"([^"]+)"')
    z_regex = re.compile(r'"z":"([^"]+)"')

    plt.ion()  # Turn on interactive mode

    duration = 2
    start_time = time.time()
    idx = 0

    while True:
        curr_time = time.time()
        if (curr_time - start_time) >= duration:
            data_speed = round(len(sensor_data[idx:]) / (curr_time - start_time), 2)
            print(f'Data Speed: {data_speed} per sec')

            idx = len(sensor_data)
            start_time = time.time()

        data = conn.recv(8192).decode()

        x_match = x_regex.search(data)
        y_match = y_regex.search(data)
        z_match = z_regex.search(data)

        if x_match and y_match and z_match:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            z = float(z_match.group(1))

            sensor_data = np.append(sensor_data, [[x, y, z]], axis=0)
            update_plot(sensor_data, line)
            plt.pause(0.01)
