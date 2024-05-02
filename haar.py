import cv2
import numpy as np  # For image processing


def identify_faces(image):
 
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Load the Haar cascade classifier for frontal face detection
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  # Detect faces in the grayscale frame
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

  # Return the list of bounding boxes for detected faces
  return faces


def process_image(image_path):

  # Load the image
  image = cv2.imread(image_path)

  # Identify faces
  faces = identify_faces(image)

  if len(faces) > 0:
    print("Found", len(faces), "faces in the image.")
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
      cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle with blue color
  else:
    print("No faces found in the image.")

  # Display the image with detected faces
  cv2.imshow("Detected Faces", image)
  cv2.waitKey(0)  # Wait for a key press to close the window
  cv2.destroyAllWindows()


def process_video():
  cap = cv2.VideoCapture(0)

  # Load the Haar cascade classifier for frontal face detection
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Identify faces in the frame
    faces = identify_faces(frame)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle with blue color

    # Display the frame with detected faces
    cv2.imshow('Live Face Detection', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break


  cap.release()
  cv2.destroyAllWindows()

user_choice = input("Enter 'i' for image processing or 'v' for video capture: ")

if user_choice.lower() == 'i':
  image_path = input("Enter the path to your image: ")
  process_image(image_path)
elif user_choice.lower() == 'v':
  process_video()
else:
  print("Invalid choice. Please enter 'i' or 'v'.")
