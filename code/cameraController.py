import cv2
import os
import time

def find_camera_device():
    """
    Find the correct /dev/video* device for the RP1-CFE camera.
    Returns the device path or raises RuntimeError if none found.
    """
    video_devices = [f"/dev/{d}" for d in os.listdir("/dev") if d.startswith("video")]
    for dev in video_devices:
        cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
        if cap.isOpened():
            # Try reading one frame to confirm it works
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                return dev
    raise RuntimeError("No working camera device found.")

def capture_image(device, filename="image.jpg", width=1280, height=720):
    cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {device}")

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Warm-up frames
    for _ in range(10):
        ret, frame = cap.read()
        if ret and frame is not None:
            time.sleep(0.05)

    # Capture final frame
    ret, frame = cap.read()
    cap.release()
    if not ret or frame is None:
        raise RuntimeError("Failed to capture image after warm-up")

    cv2.imwrite(filename, frame)
    print(f"Saved {filename} from {device}")

if __name__ == "__main__":
    device = find_camera_device()
    capture_image(device)

