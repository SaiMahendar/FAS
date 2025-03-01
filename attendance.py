import json
import cv2
import csv
import datetime
import os.path
import mediapipe as mp
import face_recognition
import numpy as np
import base64

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

with open('students.json', 'r') as f:
    student_data = []
    for line in f:
        try:
            student_data.append(json.loads(line))
        except json.JSONDecodeError:
            pass

# Initialize the webcam
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 30)  # Set the desired FPS value

# Create or open attendance file
file_path = 'attendance.csv'
if not os.path.isfile(file_path):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Time'])

# Initialize Mediapipe face detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Create a blank frame with a text field for displaying face names
blank_image = np.zeros((100, 640, 3), np.uint8)

# Initialize start time for face recognition
start_time = datetime.datetime.now()

# Initialize a set to store the names of faces already marked present
marked_faces = set()
detected_names=[]
while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        # If no frame was captured, break the loop
        break

    # Convert the frame to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe face detection
    results = face_detection.process(rgb_frame)

    # Check if any faces were detected
    if results.detections is not None:
        # Extract the first face location from the results
        detection = results.detections[0]
        ih, iw, _ = frame.shape
        bbox = detection.location_data.relative_bounding_box
        ymin, xmin, ymax, xmax = int(bbox.ymin * ih), int(bbox.xmin * iw), int(
            (bbox.ymin + bbox.height) * ih), int((bbox.xmin + bbox.width) * iw)
        face_locations = [(ymin, xmax, ymax, xmin)]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

        # Check if 5 seconds have passed since the last face recognition
        current_time = datetime.datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time >= 5:
            # Find face encodings using face_recognition
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            # Clear the detected names list
            detected_names = []

            # Loop through each face and compare with student images
            face_encoding = face_encodings[0]  # Take only the encoding of the first face
            name = None  # Declare the name variable outside the inner loop
            for student in student_data:
                if 'image_base64' in student:
                    # Decode the base64-encoded image data and load it using cv2.imdecode()
                    image_data = base64.b64decode(student['image_base64'])
                    nparr = np.frombuffer(image_data, np.uint8)
                    student_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    # Find faces in the student image
                    student_face_locations = face_recognition.face_locations(student_image)
                    student_face_encodings = face_recognition.face_encodings(student_image,
                                                                             student_face_locations)

                    # Loop through each face in the student image and compare with input image
                    for student_face_encoding in student_face_encodings:
                        match = face_recognition.compare_faces([face_encoding], student_face_encoding)[0]

                        if match:
                            # If a match is found, add the name to detected_names list
                            name = student['name']
                            detected_names.append(name)

                            # Check if the student has already been marked present today
                            now = datetime.datetime.now()
                            time = now.strftime("%Y-%m-%d %H:%M:%S")

                            # Check if the face has already been marked present
                            if name not in marked_faces:
                                # If a match is found, print the student data and add to attendance file
                                now = datetime.datetime.now()
                                name = student['name']
                                time = now.strftime("%Y-%m-%d %H:%M:%S")

                                # Check if the student has already been marked present today
                                with open(file_path, 'r') as f:
                                    reader = csv.reader(f)
                                    for row in reader:
                                        if row[0] == name and row[1][:10] == time[:10]:
                                            print(f"{name} has already been marked present today.")
                                            break
                                    else:
                                        with open(file_path, 'a', newline='') as f:
                                            writer = csv.writer(f)
                                            writer.writerow([name, time])

                                        print(f"Name: {name}\nTime: {time}")

                            # Reset the start time for the next face recognition
                            start_time = datetime.datetime.now()

                            # Break the loop after finding a match
                            break

            else:
                name = "Unknown"
                detected_names.append(name)
                print("NEW FACE DETECTED")

            # Draw the name on the frame
            cv2.putText(frame, str(name), (xmin, ymax + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



    # Update the blank image with detected face names
    blank_image[:] = (0, 0, 0)
    cv2.putText(blank_image, "Detected Faces: ", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if detected_names:
        names_text = detected_names[0]  # Take only the first detected name
    else:
        names_text = ""
    cv2.putText(blank_image, names_text, (70, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Combine the blank image with the camera view
    combined_frame = np.vstack((blank_image, frame))

    # Display the combined frame
    cv2.imshow('Video', combined_frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the video capture and destroy windows
video_capture.release()
cv2.destroyAllWindows()
