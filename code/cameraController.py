import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    raise RuntimeError("Camera not accessible")

# Warm-up
time.sleep(2)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("Failed to capture image")

cv2.imwrite("image.jpg", frame)
cap.release()

print("Saved image.jpg")

