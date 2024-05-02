import cv2

img_count = 0
# Start capturing video from the default camera
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Capture an image when 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'capturedImages/captured_image{img_count}.jpg', frame)
        img_count += 1
        print("Image captured!")

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
