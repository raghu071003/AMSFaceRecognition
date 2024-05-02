import tkinter as tk
from tkinter import messagebox
import cv2
import os
from mtcnn.mtcnn import MTCNN

# Define the directory to save captured images
capture_dir = "capturedImages"

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

def capture_image(frame, img_count, name_entry):
    """Captures an image of the detected face and saves it with user-entered name.

    Args:
        frame: The video frame containing the face.
        img_count: An integer for image naming (sequential numbering).
        name_entry: Tkinter Entry widget for entering the name.

    Returns:
        True if a face is captured and saved, False otherwise.
    """
    # Check if faces are detected
    faces = identify_faces(frame)
    if len(faces) > 0:
        # Extract face bounding box
        x, y, w, h = faces[0]['box']
        # Crop the face region from the frame
        face_image = frame[y:y + h, x:x + w]

        # Get the name entered by the user
        name = name_entry.get()

        if name:
            # Save the captured face image with user-entered name
            filename = f"{capture_dir}/{name}_{img_count}.jpg"
            cv2.imwrite(filename, face_image)
            print(f"Face captured and saved as: {filename}")
            return True
        else:
            # Show warning message if name is not entered
            messagebox.showwarning("Warning", "Please enter a name.")
            return False
    else:
        # Show warning message if no face is detected
        messagebox.showwarning("Warning", "No face detected in the frame. Make sure your face is visible.")
        return False

def capture_and_register_faces():
    """Captures an image from the webcam, detects faces, and saves the captured faces with user-entered names."""

    # Start capturing video from the default camera
    video_capture = cv2.VideoCapture(0)

    if not os.path.exists(capture_dir):
        os.makedirs(capture_dir)  # Create the directory if it doesn't exist

    img_count = 0  # Image counter

    # Create a Tkinter window for entering name
    name_window = tk.Toplevel()
    name_window.title("Enter Name")

    # Create an Entry widget for entering name
    name_label = tk.Label(name_window, text="Enter Name:")
    name_label.pack()

    name_entry = tk.Entry(name_window)
    name_entry.pack()

    def capture_with_name():
        nonlocal img_count
        ret, frame = video_capture.read()
        if ret:
            if capture_image(frame.copy(), img_count, name_entry):
                img_count += 1

    # Create a button to capture face with the entered name
    capture_button = tk.Button(name_window, text="Capture Face", command=capture_with_name)
    capture_button.pack()

    # Start the Tkinter event loop for the name window
    name_window.mainloop()

    # Release the video capture object and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

# Create the main Tkinter window
root = tk.Tk()
root.title("Face Capture")

# Create a button to start face capturing and registration
capture_button = tk.Button(root, text="Capture Face", command=capture_and_register_faces)
capture_button.pack()

# Start the Tkinter event loop
root.mainloop()
