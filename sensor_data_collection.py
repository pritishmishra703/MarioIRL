"""
sensor_data_collection.py

This script collects sensor data from a connected device over a socket connection and saves it to a CSV 
file. The data is received in JSON format and parsed using regular expressions. The script runs for a 
specified duration and saves the data at the end.

Usage:
1. Make sure the required dependencies (numpy, matplotlib) are installed.
2. Update the HOST and PORT variables to match your socket configuration.
3. Set the desired duration (in seconds) using the DURATION variable.
4. Run the script using a Python interpreter: `python sensor_data_collection.py`
"""

import os
import re
import socket
import time
import numpy as np
import pandas as pd

HOST = '192.168.56.1'
PORT = 5000
DURATION = 60

# Initialize empty lists to store the data points
sensor_data = np.empty((0, 3), float)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening for incoming connections on {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")

    # compile regex
    x_regex = re.compile(r'"x":"([^"]+)"')
    y_regex = re.compile(r'"y":"([^"]+)"')
    z_regex = re.compile(r'"z":"([^"]+)"')

    start_time = time.time()

    print('Data Collected Started!')

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= DURATION:
            break

        data = conn.recv(8192).decode()

        x_match = x_regex.search(data)
        y_match = y_regex.search(data)
        z_match = z_regex.search(data)
        
        if x_match and y_match and z_match:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            z = float(z_match.group(1))

            sensor_data = np.append(sensor_data, [[x, y, z]], axis=0)

# Save the sensor data
filename = len(os.listdir('data/raw'))

df = pd.DataFrame(sensor_data, columns=['x', 'y', 'z'])
df.to_csv(f'data/raw/{filename}.csv', index=False)
