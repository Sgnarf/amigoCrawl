from picamera2 import Picamera2
import time

# Initialize the camera
picam2 = Picamera2()

# Configure for still image
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Give the camera time to warm up
time.sleep(2)

# Take a picture
picam2.capture_file("image.jpg")

# Stop the camera
picam2.stop()

print("Picture saved as image.jpg")
