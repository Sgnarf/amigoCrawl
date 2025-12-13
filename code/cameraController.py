from picamera2 import Picamera2
from time import sleep

# --- Configuration ---
OUTPUT_FILENAME = "rotated_image.jpg"
WARMUP_TIME = 2       # Seconds to wait for the camera to adjust

# --- Script ---
try:
    print("Starting Picamera2...")
    
    # 1. Create the Picamera2 instance
    picam2 = Picamera2()

    # 2. Configure for still images
    config = picam2.create_still_configuration()

    # 3. FIX: Access Transform directly from the Picamera2 class 
    #         to apply the 180 degree rotation (vflip=True and hflip=True).
    config["transform"] = Picamera2.Transform(vflip=True, hflip=True)
    
    # Apply the configuration and start the camera
    picam2.configure(config)
    picam2.start()

    print(f"Camera started. Waiting {WARMUP_TIME} seconds for sensor warm-up...")
    sleep(WARMUP_TIME)

    print(f"Capturing image and saving to {OUTPUT_FILENAME} with 180 degree rotation...")
    
    # Capture the image
    picam2.capture_file(OUTPUT_FILENAME)

    print(f"Successfully captured and saved {OUTPUT_FILENAME}.")

except Exception as e:
    # This will catch and print any remaining errors
    print(f"An error occurred: {e}")

finally:
    # Always ensure the camera is stopped
    if 'picam2' in locals() and picam2.started:
        print("Stopping camera...")
        picam2.stop()
