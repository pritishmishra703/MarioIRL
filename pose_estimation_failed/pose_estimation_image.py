import cv2
import mediapipe as mp

# Set the flag to determine whether to show only the chest point or all points
only_chest = False

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.2, min_tracking_confidence=0.2)

# Load image
input_image_path = 'pose_estimation_failed\MarioIRL_Thumbnail.png'
image = cv2.imread(input_image_path)
height, width, _ = image.shape

# Convert the image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Perform pose estimation
results = pose.process(image_rgb)

# Extract shoulder and chest landmarks
left_shoulder = None
right_shoulder = None
chest = None

if results.pose_landmarks is not None:
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,0), thickness=5, circle_radius=20),
                              connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255), thickness=10))

# Save the image with pose estimation
output_image_path = 'result.png'
cv2.imwrite(output_image_path, image)
