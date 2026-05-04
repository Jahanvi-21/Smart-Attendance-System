import cv2
import pickle
import numpy as np
import os
from win32com.client import Dispatch

# -------------------------
# VOICE FUNCTION
# -------------------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# -------------------------
# CREATE DATA FOLDER
# -------------------------
if not os.path.exists("data"):
    os.makedirs("data")

# -------------------------
# TOTAL FACE SAMPLES
# -------------------------
TOTAL_SAMPLES = 60

# -------------------------
# CAMERA START
# -------------------------
video = cv2.VideoCapture(0)

facedetect = cv2.CascadeClassifier(
    'data/haarcascade_frontalface_default.xml'
)

# -------------------------
# CHECK CASCADE FILE
# -------------------------
if facedetect.empty():
    print("Error loading haarcascade file")
    exit()

faces_data = []
i = 0

# -------------------------
# ENTER DETAILS
# -------------------------
student_id = input("Enter Student ID: ")
name = input("Enter Student Name: ")

# Save format → ID_Name
full_name = f"{student_id}_{name}"

speak("Face registration started")

# -------------------------
# FACE CAPTURE LOOP
# -------------------------
while True:

    ret, frame = video.read()

    if not ret:
        print("Camera not working")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = facedetect.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        # Crop Face
        crop_img = frame[y:y+h, x:x+w]

        # Resize Face
        resized_img = cv2.resize(crop_img, (50, 50))

        # Store Samples
        if len(faces_data) < TOTAL_SAMPLES and i % 5 == 0:
            faces_data.append(resized_img)

        i += 1

        # Draw Rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        # Show Sample Count
        cv2.putText(
            frame,
            f"Samples: {len(faces_data)}/{TOTAL_SAMPLES}",
            (20, 40),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # Show Camera Window
    cv2.imshow("Add Faces", frame)

    key = cv2.waitKey(1)

    # Exit Conditions
    if key == ord('q') or len(faces_data) == TOTAL_SAMPLES:
        break

# -------------------------
# CLOSE CAMERA
# -------------------------
video.release()
cv2.destroyAllWindows()

# -------------------------
# CHECK MINIMUM SAMPLES
# -------------------------
faces_data = np.asarray(faces_data)

if len(faces_data) < 10:
    print("Not enough face samples captured!")
    speak("Face registration failed")
    exit()

# -------------------------
# RESHAPE DATA
# -------------------------
faces_data = faces_data.reshape(len(faces_data), -1)

# -------------------------
# SAVE DATA
# -------------------------
file_path = f"data/{full_name}.pkl"

with open(file_path, "wb") as f:
    pickle.dump(faces_data, f)

# -------------------------
# SUCCESS MESSAGE
# -------------------------
print(f"{full_name} face data saved successfully!")

speak(f"{name} registration completed")