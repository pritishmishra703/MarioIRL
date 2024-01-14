# MarioIRL

MarioIRL is a project that enables users to control Super Mario's actions in the game by mimicking their real-world movements. The system utilizes smartphone sensors, machine learning, and a custom Android app to stream accelerometer data wirelessly to a computer. This data is then used to train a machine learning model, allowing users to control Mario's movements in real-time.

Watch this YouTube Video for more information: https://www.youtube.com/watch?v=IpLV6uKAO98

## Project Overview

- **Objective**: Enable real-time control of Super Mario's actions in the game by mimicking real-world movements.
- **Key Technologies**: Accelerometer Sensor, Machine Learning, Android App Development, Python.
- **Inspiration**: The idea originated from the desire to create an interactive gaming experience without the constraints of a camera-based tracking system.

## Features

1. **Body Tracking**: Initially explored pose estimation for body tracking but transitioned to using accelerometer sensor data for more flexibility and freedom of movement.

2. **Android App**: Developed a custom Android app to stream accelerometer sensor data from the smartphone to the computer in real-time. The app facilitates wireless data transfer, eliminating the need for a camera-based tracking system.

3. **Data Collection**: Implemented a Python script to collect accelerometer sensor data during various actions such as walking, jumping, and remaining still. The collected data is stored in CSV format.

4. **Data Labeling Tool**: Created a Streamlit app for labeling the dataset, allowing for efficient labeling of chunks of data rather than individual points to enhance the model's accuracy.

5. **Machine Learning Model**: Trained a simple neural network using the collected and labeled accelerometer data to predict user actions. Achieved a 95% accuracy on the training set.

6. **Integration with Super Mario**: Integrated the machine learning model with the Super Mario gameplay through Python scripting. Users can control Mario's actions by mimicking specific movements.
