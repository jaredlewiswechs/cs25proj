import cv2
import time
import os

# --- Configuration ---
# Make sure 'haarcascade_frontalface_default.xml' is in the same folder as this script!
CASCADE_PATH = 'haarcascade_frontalface_default.xml'
RECTANGLE_COLOR = (0, 255, 0) # Color of the rectangle (BGR format)
RECTANGLE_THICKNESS = 2
FRAME_WIDTH = 640 # Optional: Set a specific width for the webcam frame
FRAME_HEIGHT = 480 # Optional: Set a specific height
# ---------------------

def check_cascade_file(path):
    """Checks if the cascade file exists."""
    if not os.path.exists(path):
        print(f"ERROR: Cascade file not found at '{path}'")
        print("Please download 'haarcascade_frontalface_default.xml' from the OpenCV GitHub")
        print("and place it in the same directory as this script.")
        print("Link: https://github.com/opencv/opencv/tree/master/data/haarcascades")
        return False
    return True

def run_face_detection():
    """Captures webcam feed and performs real-time face detection."""

    if not check_cascade_file(CASCADE_PATH):
        return

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if face_cascade.empty():
        print("ERROR: Could not load cascade classifier!")
        print(f"Is the file '{CASCADE_PATH}' corrupted or incorrect?")
        return

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("ERROR: Could not open webcam!")
        print("Is it connected and enabled? Do you have the right camera index (0, 1, ...)?")
        return

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print("\nStarting face detection...")
    print("Look at the webcam!")
    print("Press 'q' in the video window to quit.")

    last_detection_time = time.time()
    detection_interval = 0.1

    faces = [] # <<< --- ADD THIS LINE: Initialize faces before the loop starts (or just inside)

    while True:
        # ADD INITIALIZATION INSIDE THE LOOP TO BE SAFER
        faces_in_this_frame = () # Initialize/reset for this specific frame iteration

        ret, frame = video_capture.read()
        if not ret:
            print("ERROR: Failed to capture frame from webcam.")
            break

        frame = cv2.flip(frame, 1)

        current_time = time.time()
        if current_time - last_detection_time > detection_interval:
            last_detection_time = current_time
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces and assign to the variable for this frame
            faces_in_this_frame = face_cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40)
            )

        # Now, loop over the faces detected *in this frame's detection cycle*
        # If detection didn't run, faces_in_this_frame will be the empty tuple ()
        for (x, y, w, h) in faces_in_this_frame:
            cv2.rectangle(frame, (x, y), (x+w, y+h), RECTANGLE_COLOR, RECTANGLE_THICKNESS)

        cv2.imshow('Face Detection - Press Q to Quit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Webcam released and windows closed.")

    # When everything is done, release the capture and destroy windows
    video_capture.release()
    cv2.destroyAllWindows()
    print("Webcam released and windows closed.")

# --- Main Execution ---
if __name__ == "__main__":
    run_face_detection()