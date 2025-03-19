#
#
# import cv2
# import numpy as np
#
#
# def measure_face():
#     # Load the pre-trained face detection model (Haarcascade)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
#     # Configuration parameters
#     MAX_WIDTH = 300  # Maximum allowed width in pixels
#     MAX_HEIGHT = 300  # Maximum allowed height in pixels
#
#     # Try accessing the camera
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return
#
#     last_measurement = None
#     last_face_color = None
#
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Failed to capture image.")
#             break
#
#         # Convert frame to grayscale (improves detection accuracy)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#         # Detect faces
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#
#         for (x, y, w, h) in faces:
#             # Draw a rectangle around the face
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#             # Display face width and height
#             text = f"Width: {w}px, Height: {h}px"
#             cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#
#             # Store the last measured dimensions
#             last_measurement = (w, h)
#
#             # Check if detected face exceeds limits
#             if w > MAX_WIDTH or h > MAX_HEIGHT:
#                 print(f"Warning: Detected face exceeds size limit! Width: {w}px, Height: {h}px")
#
#             # Extract face region
#             face_region = frame[y:y + h, x:x + w]
#
#             # Compute the average color of the face region
#             avg_color_per_row = np.mean(face_region, axis=0)
#             avg_color = np.mean(avg_color_per_row, axis=0)
#             last_face_color = avg_color.astype(int)
#
#         # Display the output
#         cv2.imshow('Face Measurement', frame)
#
#         # Press 'q' to exit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the capture and close windows
#     cap.release()
#     cv2.destroyAllWindows()
#
#     # Print the last measured face dimensions and color
#     if last_measurement:
#         print(f"Last Measured Face - Width: {last_measurement[0]}px, Height: {last_measurement[1]}px")
#     else:
#         print("No face was measured.")
#
#     if last_face_color is not None:
#         print(f"Estimated Face Color (BGR): {last_face_color}")
#     else:
#         print("No face color detected.")
#
#
# if __name__ == "__main__":
#     measure_face()


import cv2
import numpy as np

# Define size limits
MAX_WIDTH = 300
MAX_HEIGHT = 300

# Create background subtractor (MOG2 is good for motion detection)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)


def detect_moving_stone():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply background subtraction (detect motion)
        fg_mask = bg_subtractor.apply(gray)

        # Apply threshold to remove noise
        _, thresh = cv2.threshold(fg_mask, 50, 255, cv2.THRESH_BINARY)

        # Find contours (moving objects)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Filter out very small objects (noise)
            if w > 30 and h > 30:
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display width & height
                text = f"Width: {w}px, Height: {h}px"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Check if stone size exceeds limit
                if w > MAX_WIDTH or h > MAX_HEIGHT:
                    print(f"Warning: Large moving stone detected! Width: {w}px, Height: {h}px")

        # Show frame
        cv2.imshow("Moving Stone Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_moving_stone()
