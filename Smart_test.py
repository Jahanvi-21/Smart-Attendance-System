import cv2
import os
import csv
import pickle
import numpy as np
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch

# -----------------------------
# VOICE FUNCTION
# -----------------------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# -----------------------------
# SETTINGS
# -----------------------------
DATA_DIR = "data/"
ATT_FILE = "Attendance.csv"
BG_IMAGE = "background.png"
CAM_INDEX = 0

# -----------------------------
# LOAD DATA
# -----------------------------
faces = []
labels = []

for file in os.listdir(DATA_DIR):

    if file.endswith(".pkl"):

        with open(os.path.join(DATA_DIR, file), "rb") as f:

            data = pickle.load(f)

            label = file[:-4]

            for face in data:

                face = np.array(face).flatten()

                if face.shape[0] == 7500:
                    faces.append(face)
                    labels.append(label)

if len(faces) == 0:
    print("No face data found!")
    exit()

faces = np.array(faces)
labels = np.array(labels)

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("Training Model...")

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(faces, labels)

print("Model Ready!")

# -----------------------------
# FACE DETECTOR
# -----------------------------
faceDetect = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# -----------------------------
# ATTENDANCE FUNCTION
# -----------------------------
def mark_attendance(name):

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")
    current_time = now.strftime("%H:%M:%S")

    already_marked = False

    if os.path.exists(ATT_FILE):

        with open(ATT_FILE, "r") as f:

            reader = csv.reader(f)

            for row in reader:

                if len(row) >= 3:

                    if row[0] == name and row[2] == date:
                        already_marked = True
                        break

    if not already_marked:

        student_name = name.split("_")[0]
        student_id = name.split("_")[1]

        with open(ATT_FILE, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                student_name,
                student_id,
                date,
                current_time
            ])

        speak(f"{student_name}, attendance marked")

        return current_time

    return None

# -----------------------------
# GET TODAY DATA
# -----------------------------
def get_today_data():

    today = datetime.now().strftime("%d-%m-%Y")

    entries = []

    if os.path.exists(ATT_FILE):

        with open(ATT_FILE, "r") as f:

            reader = csv.reader(f)

            for row in reader:

                if len(row) >= 4 and row[2] == today:
                    entries.append(row)

    return entries

# -----------------------------
# CAMERA START
# -----------------------------
video = cv2.VideoCapture(CAM_INDEX)

last_name = "No Detection"
last_time = "--:--:--"

marked_names = set()

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    ret, frame = video.read()

    if not ret:
        break

    frame = cv2.resize(frame, (900, 650))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in detected_faces:

        crop = frame[y:y+h, x:x+w]

        resized = cv2.resize(crop, (50, 50)).flatten().reshape(1, -1)

        # -----------------------------
        # PREDICT FACE
        # -----------------------------
        distances, indices = knn.kneighbors(
            resized,
            n_neighbors=1
        )

        distance = distances[0][0]

        if distance > 5000:

            name = "Unknown"

        else:

            name = knn.predict(resized)[0]

        # -----------------------------
        # DRAW FACE BOX
        # -----------------------------
        cv2.rectangle(frame,
                      (x, y),
                      (x+w, y+h),
                      (0, 255, 0),
                      2)

        cv2.putText(frame,
                    name,
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        # -----------------------------
        # AUTO ATTENDANCE
        # -----------------------------
        if name != "Unknown" and name not in marked_names:

            tm = mark_attendance(name)

            if tm:

                last_name = name
                last_time = tm

                marked_names.add(name)

    # -----------------------------
    # LOAD BACKGROUND
    # -----------------------------
    bg = cv2.imread(BG_IMAGE)

    if bg is None:
        bg = np.zeros((800, 1600, 3), dtype=np.uint8)

    bg = cv2.resize(bg, (1600, 800))

    bg[120:770, 30:930] = frame

    # -----------------------------
    # DATE & TIME
    # -----------------------------
    now = datetime.now()

    date = now.strftime("%d-%m-%Y")

    live_time = now.strftime("%H:%M:%S")

    entries = get_today_data()

    present = len(entries)

    total_students = 50

    absent = total_students - present

    attendance_percent = 0

    if total_students > 0:
        attendance_percent = int(
            (present / total_students) * 100
        )

    # -----------------------------
    # UI TEXT
    # -----------------------------
    cv2.putText(bg, date, (1080, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(bg, live_time, (1320, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(bg, "LAST DETECTED", (1030, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,255),
                2)

    cv2.putText(bg, f"Name: {last_name}", (1030, 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,255),
                2)

    cv2.putText(bg, f"Time: {last_time}", (1030, 270),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,255),
                2)

    cv2.putText(bg, f"Present: {present}", (1030, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2)

    cv2.putText(bg, f"Absent: {absent}", (1250, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2)

    cv2.putText(bg,
                f"Attendance: {attendance_percent}%",
                (1030, 400),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,0,255),
                2)

    cv2.putText(bg,
                "RECENT ENTRIES",
                (1030, 470),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2)

    # -----------------------------
    # SHOW RECENT ENTRIES
    # -----------------------------
    y = 520

    for row in entries[-5:][::-1]:

        txt = f"{row[0]} ({row[1]})  {row[3]}"

        cv2.putText(bg,
                    txt,
                    (1030, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255,255,255),
                    2)

        y += 40

    # -----------------------------
    # SHOW WINDOW
    # -----------------------------
    cv2.imshow("Face Recognition Attendance", bg)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# -----------------------------
# CLOSE
# -----------------------------
video.release()

cv2.destroyAllWindows()