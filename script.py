import cv2
import requests
import time
import base64
import os
import random
import string

# Configuration
ENDPOINT_URL = "https://webcam.connect.prusa3d.com/c/snapshot"
TOKEN = ""  # Replace with your actual token
INTERVAL = 10  # seconds between snapshots

def capture_image():
    try:
        # Initialize the camera
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return None
        print("Camera opened successfully.")
        
        # Set camera properties (brightness, contrast, exposure, etc.)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 25)
        cap.set(cv2.CAP_PROP_MODE, 1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        
        # Capture a frame
        ret, frame = cap.read()
        ret, frame = cap.read()
        ret, frame = cap.read()
        ret, frame = cap.read()
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return None
        print("Frame captured successfully.")
        
        # Release the camera
        cap.release()
        print("Camera released successfully.")
        
        # Encode the frame as JPEG
        ret, img_encoded = cv2.imencode('.jpg', frame)
        if not ret:
            print("Error: Could not encode image.")
            return None
        print("Image encoded successfully.")
        
        return img_encoded
    except Exception as e:
        print(f"Error capturing image: {e}")
        return None

def upload_snapshot(image):
    # Prepare headers
    headers = {
        'Content-Type': 'image/jpg',
        'token': TOKEN,
        'fingerprint': "BLACKPRINTERCAM2024"
    }
    
    # Upload image
    try:
        response = requests.put(
            ENDPOINT_URL,
            headers=headers,
            data=image.tobytes()
        )
        print(f"Upload response status code: {response.status_code}")
        print(f"Upload response content: {response.content}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error uploading snapshot: {e}")
        return False

def main():
    while True:
        try:
            # Capture image
            image = capture_image()
            if image is not None:
                # Upload image
                if upload_snapshot(image):
                    print("Snapshot uploaded successfully")
                else:
                    print("Failed to upload snapshot")
            
            # Wait for the next interval
            time.sleep(INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping snapshot service")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
