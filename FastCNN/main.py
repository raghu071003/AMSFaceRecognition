import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import face_recognition
from PIL import Image, ImageTk

def load_reference_images(folder_path):
    reference_encodings = []
    reference_names = []

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            reference_encodings.append(encoding)
            reference_names.append((filename, image_path))  # Store both filename and image path

    return reference_encodings, reference_names

def detect_faces_and_compare(target_image_path, reference_encodings, reference_names):
    # Load the target image
    target_image = face_recognition.load_image_file(target_image_path)

    # Find all face locations and encodings in the target image
    face_locations = face_recognition.face_locations(target_image)
    target_encodings = face_recognition.face_encodings(target_image, face_locations)

    # Compare the face encodings of the target image with the reference images
    matched_images = []
    matched_image_paths = []  # Store matched image paths
    unmatched_count = 0

    for target_encoding in target_encodings:
        matches = face_recognition.compare_faces(reference_encodings, target_encoding)
        if any(matches):
            matched_index = matches.index(True)
            matched_images.append(reference_names[matched_index][0])  # Store matched filename
            matched_image_paths.append(reference_names[matched_index][1])  # Store matched image path
        else:
            unmatched_count += 1

    return matched_images, matched_image_paths, unmatched_count

def select_target_image():
    target_image_path = filedialog.askopenfilename(title="Select Target Image")
    target_image_entry.delete(0, tk.END)
    target_image_entry.insert(0, target_image_path)

def select_reference_folder():
    reference_folder_path = filedialog.askdirectory(title="Select Reference Folder")
    reference_folder_entry.delete(0, tk.END)
    reference_folder_entry.insert(0, reference_folder_path)

def process_image():
    target_image_path = target_image_entry.get()
    if not target_image_path:
        messagebox.showerror("Error", "Please select a target image.")
        return

    reference_folder = reference_folder_entry.get()
    if not reference_folder:
        messagebox.showerror("Error", "Please select the reference images folder.")
        return

    reference_encodings, reference_names = load_reference_images(reference_folder)

    matched_images, matched_image_paths, unmatched_count = detect_faces_and_compare(target_image_path, reference_encodings, reference_names)

    # Display the matched images in a separate window
    if matched_images:
        matched_window = tk.Toplevel()
        matched_window.title("Matched Images")

        row, col = 0, 0
        for matched_image, matched_image_path in zip(matched_images, matched_image_paths):
            image = Image.open(matched_image_path)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(matched_window, text=os.path.splitext(matched_image)[0])  # Display filename without extension
            label.grid(row=row, column=col)

            img_label = tk.Label(matched_window, image=photo)
            img_label.grid(row=row+1, column=col)

            img_label.photo = photo  # Keep a reference to avoid garbage collection

            col += 1
            if col >= 3:  # Display 3 images per row
                row += 2
                col = 0

    messagebox.showinfo("Result", f"Matched images: {matched_images}\nUnmatched faces count: {unmatched_count}")

# Create the main window
root = tk.Tk()
root.title("Face Detection and Comparison")

# Create and place widgets
target_image_label = tk.Label(root, text="Target Image:")
target_image_label.grid(row=0, column=0)

target_image_entry = tk.Entry(root, width=50)
target_image_entry.grid(row=0, column=1)

browse_target_button = tk.Button(root, text="Browse", command=select_target_image)
browse_target_button.grid(row=0, column=2)

reference_folder_label = tk.Label(root, text="Reference Folder:")
reference_folder_label.grid(row=1, column=0)

reference_folder_entry = tk.Entry(root, width=50)
reference_folder_entry.grid(row=1, column=1)

browse_reference_button = tk.Button(root, text="Browse", command=select_reference_folder)
browse_reference_button.grid(row=1, column=2)

process_button = tk.Button(root, text="Process", command=process_image)
process_button.grid(row=2, column=1)

# Start the GUI event loop
root.mainloop()
