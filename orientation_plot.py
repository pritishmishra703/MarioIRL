import re
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

HOST = '192.168.97.32'
PORT = 5000

sensor_data = np.empty((0, 3), float)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening for incoming connections on {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")

    x_regex = re.compile(r'"x":"([^"]+)"')
    y_regex = re.compile(r'"y":"([^"]+)"')
    z_regex = re.compile(r'"z":"([^"]+)"')

    start_time = time.time()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 10)

    while True:
        data = conn.recv(8192).decode()

        x_match = x_regex.search(data)
        y_match = y_regex.search(data)
        z_match = z_regex.search(data)

        if x_match and y_match and z_match:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            z = float(z_match.group(1))

            sensor_data = np.append(sensor_data, np.array([[x, y, z]]), axis=0)
            ax.clear()
            xx, yy = np.meshgrid(np.linspace(0, 10, 10), np.linspace(0, 10, 10))
            zz = (sensor_data[-1, 0] * xx + sensor_data[-1, 1] * yy) / sensor_data[-1, 2]
            ax.plot_surface(xx, yy, zz, alpha=0.5)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.axis('off')
            ax.set_box_aspect([np.ptp(arr) for arr in [xx, yy, zz]])
            plt.draw()
            plt.pause(0.1)
