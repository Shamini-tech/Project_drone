import cv2
import time

def get_frame():
    cap = cv2.VideoCapture("sim_assets/sample_feed.mp4")
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video
            continue
        yield frame
        time.sleep(1/30)  # simulate 30 FPS
