import cv2
import mediapipe as mp

# Set the flag to determine whether to show only the chest point or all points
only_chest = False

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.2, min_tracking_confidence=0.2)

# Open video capture
input_video_path = r'C:\Users\priti\Videos\MarioIRL\box.mp4'
cap = cv2.VideoCapture(input_video_path)

# Get video properties
width = int(cap.get(3))
height = int(cap.get(4))
fps = cap.get(5)

# Define the codec and create a VideoWriter object
output_video_path = r'C:\Users\priti\Videos\MarioIRL\BoxPose.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform pose estimation
    results = pose.process(frame_rgb)

    # Extract shoulder and chest landmarks
    left_shoulder = None
    right_shoulder = None
    chest = None

    if only_chest and results.pose_landmarks is not None:
        for i, landmark in enumerate(results.pose_landmarks.landmark):
            cx, cy = int(landmark.x * width), int(landmark.y * height)

            # Check if it's a shoulder point
            if i == 11:  # LEFT SHOULDER
                left_shoulder = (cx, cy)
            elif i == 12:  # RIGHT SHOULDER
                right_shoulder = (cx, cy)

            # Check if it's a chest point
            if left_shoulder is not None and right_shoulder is not None:
                chest = ((left_shoulder[0] + right_shoulder[0]) // 2, (left_shoulder[1] + right_shoulder[1]) // 2)
                chest = list(chest)
                chest[1] += 100
                break

    if only_chest and chest is not None:
        # Draw only chest point
        cv2.circle(frame, chest, 10, (0, 255, 0), -1)
        cv2.putText(frame, f'({chest[0]}, {chest[1]})', (chest[0]-330, chest[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 8)

    else:
        # Draw all points
        if results.pose_landmarks is not None:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Write the frame with pose estimation to the output video
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()
