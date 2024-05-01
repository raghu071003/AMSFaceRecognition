import cv2
import numpy as np
import os
from mtcnn.mtcnn import MTCNN

# Define the directory to save captured images
capture_dir = "register_faces"

def identify_faces(image):
  """Identifies faces in the image using MTCNN.

  Args:
      image: The image to process.

  Returns:
      A list of dictionaries containing face detections (bounding boxes).
  """
  # Create an MTCNN detector
  detector = MTCNN()
  
  # Detect faces
  faces = detector.detect_faces(image)
  
  # Return the list of detections (bounding boxes)
  return faces

def capture_image(frame, img_count):
  """Captures an image of the detected face and saves it with user-entered name.

  Args:
      frame: The video frame containing the face.
      img_count: An integer for image naming (sequential numbering).
  """
  # Check if faces are detected
  faces = identify_faces(frame)
  if len(faces) > 0:
    # Extract face bounding box
    x, y, w, h = faces[0]['box']
    # Crop the face region from the frame
    face_image = frame[y:y+h, x:x+w]

    # Prompt user for name
    name = input("Enter name for captured image: ")

    # Save the captured face image with user-entered name
    filename = f"{capture_dir}/{name}_{img_count}.jpg"
    cv2.imwrite(filename, face_image)
    print(f"Face captured and saved as: {filename}")

# Start capturing video from the default camera
video_capture = cv2.VideoCapture(0)

if not os.path.exists(capture_dir):
  os.makedirs(capture_dir)  # Create the directory if it doesn't exist

img_count = 0  # Image counter

while True:
  # Capture frame-by-frame
  ret, frame = video_capture.read()

  # Display the resulting frame
  cv2.imshow('Video', frame)

  # Capture an image when 's' is pressed
  if cv2.waitKey(1) & 0xFF == ord('s'):
    capture_image(frame.copy(), img_count)  # Copy frame to avoid modifying original
    img_count += 1

  # Exit the loop if 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
