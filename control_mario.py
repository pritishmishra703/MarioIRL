import threading
import keyboard
import time
import numpy as np
import socket
import re

# set jax backend
import os
os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras

# load model
model = keras.models.load_model('models/model_01.keras')

# Initialize variables
HOST = '192.168.97.32'
PORT = 5000
window_size = 14
shift_size = int(window_size * 0.25)
jumped = time.time()
prev_pred_class = None
pressed_key = None

# Initialize empty lists to store the data points
sensor_data = np.empty((0, 3), float)

# classes
classes = ['jumping', 'still', 'walking']

# jump right release
def jump_release():
    time.sleep(1)
    keyboard.release('up')
    keyboard.release('right')

# predict function
def predict_model(data):
    global jumped, pressed_key, prev_pred_class
    inp = np.expand_dims(data, axis=0)
    pred = model(inp)
    conf = np.max(pred[0])
    pred = np.argmax(pred, -1)[0]
    
    if conf <= 0.6:
        pred = 1

    pred_class = classes[pred]
    print(pred_class, pressed_key)

    if prev_pred_class != pred_class:
        if pressed_key == 'right':
            keyboard.release('right')

        pressed_key = None

    if (pred_class == 'jumping') and (time.time() - jumped) > 1:
        keyboard.press('right')
        keyboard.press('up')
        jumped = time.time()
        thread = threading.Thread(target=jump_release)
        thread.start()
        pressed_key = 'up'
    
    elif (pred_class == 'walking') and (pressed_key != 'right'):
        keyboard.press('right')
        pressed_key = 'right'
    
    elif pred_class == 'still':
        if pressed_key == 'right':
            keyboard.release('right')
        
        pressed_key = None
    
    prev_pred_class = pred_class

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

    while True:
        data = conn.recv(8192).decode()

        x_match = x_regex.search(data)
        y_match = y_regex.search(data)
        z_match = z_regex.search(data)

        if x_match and y_match and z_match:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            z = float(z_match.group(1))
            sensor_data = np.append(sensor_data, [[x, y, z]], axis=0)

            if sensor_data.shape[0] == window_size:
                prediction_thread = threading.Thread(target=predict_model, args=(sensor_data,))
                prediction_thread.start()
                sensor_data = sensor_data[shift_size:]
