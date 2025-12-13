import subprocess
import cv2
import os

def capture_image(filename="image.jpg"):
    # Use libcamera-still to capture image from the RPi5 camera
    # --nopreview avoids opening a window
    result = subprocess.run(["libcamera-still", "-o", filename, "--nopreview"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"libcamera-still failed:\n{result.stderr.decode()}")
    if not os.path.exists(filename):
        raise RuntimeError("Image file not created.")
    
    # Read captured image with OpenCV
    img = cv2.imread(filename)
    if img is None:
        raise RuntimeError("Failed to load captured image with OpenCV.")
    return img

if __name__ == "__main__":
    image = capture_image("image.jpg")
    print("Captured image.jpg successfully!")
    print("Image shape:", image.shape)
