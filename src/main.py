# import cv2
# import mediapipe as mp
# import numpy as np
# import argparse
# from src.firebase_service import save_to_firebase


# # Mediapipe initialization
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# # Global variables
# counter = 0
# stage = None  # Can be "up" or "down"

# def calculate_angle(a, b, c):
#     """
#     Calculate the angle between three points.
#     Points: a, b, c as tuples of (x, y).
#     """
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle
#     return angle


# def process_frame(image, pose):
#     """Process each frame and update squat counter."""
#     global counter, stage

#     # Recolor frame to RGB
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image_rgb.flags.writeable = False

#     # Detect pose
#     results = pose.process(image_rgb)

#     # Recolor back to BGR for OpenCV
#     image_rgb.flags.writeable = True
#     image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

#     try:
#         landmarks = results.pose_landmarks.landmark

#         # Get coordinates (Right hip, knee, ankle for squat)
#         hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
#                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#         knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
#                 landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
#         ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
#                  landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

#         # Calculate angle
#         angle = calculate_angle(hip, knee, ankle)

#         # Display angle near knee
#         cv2.putText(image, str(int(angle)),
#                     tuple(np.multiply(knee, [640, 480]).astype(int)),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#         # Counter Logic
#         if angle > 160:
#             stage = "up"
#         if angle < 70 and stage == "up":
#             stage = "down"
#             counter += 1
#             print(f"[INFO] Rep Count: {counter}")

#             # Save to Firebase (non-blocking)
#             try:
#                 save_to_firebase(counter, stage)
#             except Exception as e:
#                 print(f"[WARNING] Firebase save failed: {e}")

#     except Exception as e:
#         print(f"[DEBUG] Pose processing error: {e}")

#     # Draw mediapipe landmarks
#     if results.pose_landmarks:
#         mp_drawing.draw_landmarks(
#             image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
#             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
#         )

#     return image


# def display_ui(image):
#     """Display counter and stage UI overlay."""
#     cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

#     # Reps
#     cv2.putText(image, 'REPS', (15, 12),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#     cv2.putText(image, str(counter), (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

#     # Stage
#     cv2.putText(image, 'STAGE', (65, 12),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#     cv2.putText(image, stage if stage else "-", (60, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)


# def main(video_path=None):
#     """Main function to run squat detection."""
#     cap = cv2.VideoCapture(0 if video_path is None else video_path)

#     if not cap.isOpened():
#         print("[ERROR] Cannot open camera or video.")
#         return

#     with mp_pose.Pose(min_detection_confidence=0.5,
#                       min_tracking_confidence=0.5) as pose:
#         print("[INFO] Pose detection started. Press 'q' to quit.")

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("[ERROR] Failed to grab frame.")
#                 break

#             # Process frame
#             frame = process_frame(frame, pose)

#             # Display UI overlay
#             display_ui(frame)

#             # Show final output
#             cv2.imshow('Squat Counter', frame)

#             # Exit on 'q'
#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 print("[INFO] Exiting squat detection.")
#                 break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Squat Counter using Mediapipe and Firebase")
#     parser.add_argument('--video', type=str, default=None, help="Path to video file (leave empty for webcam).")
#     args = parser.parse_args()

#     main(args.video)


import cv2
import mediapipe as mp
import numpy as np
from src.firebase_service import save_to_firebase

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Counter variables
counter = 0
stage = None  # Can be "up" or "down"

def calculate_angle(a, b, c):
    """Calculate the angle between three points (a, b, c)."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def main(use_webcam=True, video_path=None, display_window=True):
    """
    Main function for pose detection.
    
    Args:
        use_webcam (bool): If True, use webcam as input.
        video_path (str): Optional path to a video file.
        display_window (bool): If True, display OpenCV window.
    """
    global counter, stage

    if use_webcam:
        cap = cv2.VideoCapture(0)
    elif video_path:
        cap = cv2.VideoCapture(video_path)
    else:
        raise ValueError("Either set use_webcam=True or provide a video_path.")

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Recolor frame to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Detect pose
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Extract hip, knee, and ankle coordinates for squat detection
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate the angle
                angle = calculate_angle(hip, knee, ankle)

                # Display angle near the knee
                cv2.putText(image, str(int(angle)),
                            tuple(np.multiply(knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Counter logic
                if angle > 160:
                    stage = "up"
                if angle < 70 and stage == "up":
                    stage = "down"
                    counter += 1
                    print(f"Counter: {counter}")
                    save_to_firebase(counter, stage)

            except Exception as e:
                print("Pose detection error:", e)

            # Display counter on screen
            cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            if display_window:
                cv2.imshow('Pose Detection', image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()
