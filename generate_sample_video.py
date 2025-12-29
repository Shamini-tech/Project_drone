import cv2
import numpy as np
import os

# Ensure folder exists
os.makedirs("sim_assets", exist_ok=True)

# Video settings
width, height = 320, 240
fps = 30
duration = 5  # seconds
frames = fps * duration

out = cv2.VideoWriter('sim_assets/sample_feed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for i in range(frames):
    # Generate a colorful moving rectangle
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.rectangle(frame, (i % width, 50), ((i+50) % width, 150), (0, 255, 0), -1)
    out.write(frame)

out.release()
print("Sample video created at sim_assets/sample_feed.mp4")
