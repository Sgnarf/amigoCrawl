import cv2
import time

DEVICE = "/dev/video0"

cap = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)

if not cap.isOpened():
    raise RuntimeError(f"Could not open camera {DEVICE}")

# Optional: set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Warm up
time.sleep(2)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("Failed to capture image")

cv2.imwrite("image.jpg", frame)

cap.release()
print("Saved image.jpg")
