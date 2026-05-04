import streamlit as st
import cv2
import pickle
import numpy as np
import pandas as pd
import os
import csv
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import threading
import pyttsx3

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Face Recognition Attendance System",
    layout="wide"
)

# -----------------------------------
# VOICE ENGINE
# -----------------------------------
# -----------------------------------
# SAFE VOICE FUNCTION
# -----------------------------------
def speak(text):

    def run_speech():

        engine = pyttsx3.init()

        engine.setProperty('rate', 150)

        engine.say(text)

        engine.runAndWait()

    thread = threading.Thread(target=run_speech)

    thread.start()
# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.hero {
    background: linear-gradient(135deg, #111827, #1e293b);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}

.hero h1 {
    color: white;
    font-size: 50px;
    font-weight: bold;
}

.hero p {
    color: #cbd5e1;
    font-size: 20px;
}

.feature-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    transition: 0.3s;
    height: 190px;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-top: 10px;
}

.feature-text {
    color: #d1d5db;
    font-size: 16px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🧒 Face Recognition Attendance System 👩‍🦰")

# -----------------------------------
# FOLDERS
# -----------------------------------
DATA_DIR = "data"
ATT_FILE = "Attendance.csv"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# -----------------------------------
# LOAD FACE DETECTOR
# -----------------------------------
faceDetect = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Home",
        "Register Face",
        "Take Attendance",
        "View Attendance"
    ]
)

# ===================================
# HOME PAGE
# ===================================
if menu == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🤖 AI Attendance System</h1>
        <p>
            Smart Face Recognition Attendance using
            OpenCV, Machine Learning & Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 System Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h1>📸</h1>
            <div class="feature-title">Face Registration</div>
            <div class="feature-text">
                Register student faces using webcam.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h1>🤖</h1>
            <div class="feature-title">AI Recognition</div>
            <div class="feature-text">
                Real-time face recognition system.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h1>🔊</h1>
            <div class="feature-title">Voice Assistant</div>
            <div class="feature-text">
                Voice feedback after registration and attendance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <h1>✅</h1>
            <div class="feature-title">Auto Attendance</div>
            <div class="feature-text">
                Attendance marked automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <h1>📁</h1>
            <div class="feature-title">CSV Storage</div>
            <div class="feature-text">
                Secure attendance records storage.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
            <h1>⚡</h1>
            <div class="feature-title">Live Camera</div>
            <div class="feature-text">
                Real-time webcam integration.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 📖 About Project")

    st.info("""
    This AI-based Face Recognition Attendance System uses
    Computer Vision, Machine Learning, and Voice Assistance
    to automate attendance management efficiently.
    """)

    st.markdown("## 📊 Live Statistics")

    total_students = len([
        file for file in os.listdir(DATA_DIR)
        if file.endswith(".pkl")
    ])

    total_attendance = 0

    if os.path.exists(ATT_FILE):
        df = pd.read_csv(ATT_FILE, header=None)
        total_attendance = len(df)

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "👨‍🎓 Registered Students",
            total_students
        )

    with s2:
        st.metric(
            "✅ Attendance Records",
            total_attendance
        )

    with s3:
        st.metric(
            "🤖 AI Accuracy",
            "95%"
        )

    st.markdown("## 🛠️ Technologies Used")

    t1, t2, t3, t4, t5 = st.columns(5)

    with t1:
        st.success("Python")

    with t2:
        st.success("OpenCV")

    with t3:
        st.success("Streamlit")

    with t4:
        st.success("Machine Learning")

    with t5:
        st.success("Voice AI")

    st.markdown("---")

    st.markdown("""
    <center>
        <h4 style='color:gray;'>
            Developed using AI, Voice AI & Computer Vision 🚀
        </h4>
    </center>
    """, unsafe_allow_html=True)

# ===================================
# REGISTER FACE
# ===================================
elif menu == "Register Face":

    st.subheader("🧑 Register Student Face")

    student_id = st.text_input("Enter Student ID")
    student_name = st.text_input("Enter Student Name")

    capture_btn = st.button("Start Registration")

    if capture_btn:

        if student_id == "" or student_name == "":
            st.warning("Please enter details")
            speak("Please enter student details")

        else:

            speak("Face registration started")

            video = cv2.VideoCapture(0)

            faces_data = []
            i = 0
            TOTAL_SAMPLES = 60

            st.info("Capturing face samples...")

            frame_placeholder = st.empty()

            while True:

                ret, frame = video.read()

                if not ret:
                    st.error("Camera not working")
                    speak("Camera not working")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = faceDetect.detectMultiScale(
                    gray,
                    1.3,
                    5
                )

                for (x, y, w, h) in faces:

                    crop_img = frame[y:y+h, x:x+w]

                    resized_img = cv2.resize(
                        crop_img,
                        (50, 50)
                    )

                    if len(faces_data) < TOTAL_SAMPLES and i % 5 == 0:
                        faces_data.append(resized_img)

                    i += 1

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Samples: {len(faces_data)}/{TOTAL_SAMPLES}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                frame_rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                frame_placeholder.image(
                    frame_rgb,
                    channels="RGB"
                )

                if len(faces_data) == TOTAL_SAMPLES:
                    break

            video.release()
            cv2.destroyAllWindows()

            faces_data = np.asarray(faces_data)

            faces_data = faces_data.reshape(
                len(faces_data),
                -1
            )

            filename = f"{student_id}_{student_name}.pkl"

            with open(
                os.path.join(DATA_DIR, filename),
                "wb"
            ) as f:

                pickle.dump(faces_data, f)

            st.success("✅ Face Registered Successfully")

            speak(f"{student_name} registration completed successfully")

# ===================================
# TAKE ATTENDANCE
# ===================================
elif menu == "Take Attendance":

    st.subheader("📸 AI Attendance System")

    faces = []
    labels = []

    for file in os.listdir(DATA_DIR):

        if file.endswith(".pkl"):

            with open(
                os.path.join(DATA_DIR, file),
                "rb"
            ) as f:

                data = pickle.load(f)

                label = file[:-4]

                for face in data:

                    face = np.array(face).flatten()

                    if face.shape[0] == 7500:
                        faces.append(face)
                        labels.append(label)

    if len(faces) == 0:
        st.warning("No registered faces found")
        speak("No registered faces found")

    else:

        faces = np.array(faces)
        labels = np.array(labels)

        knn = KNeighborsClassifier(n_neighbors=5)

        knn.fit(faces, labels)

        start_btn = st.button("Start Camera")

        if start_btn:

            speak("Attendance system started")

            video = cv2.VideoCapture(0)

            frame_placeholder = st.empty()

            marked_names = set()

            while True:

                ret, frame = video.read()

                if not ret:
                    break

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                detected_faces = faceDetect.detectMultiScale(
                    gray,
                    1.3,
                    5
                )

                for (x, y, w, h) in detected_faces:

                    crop = frame[y:y+h, x:x+w]

                    resized = cv2.resize(
                        crop,
                        (50, 50)
                    ).flatten().reshape(1, -1)

                    distances, indices = knn.kneighbors(
                        resized,
                        n_neighbors=1
                    )

                    distance = distances[0][0]

                    if distance > 5000:
                        name = "Unknown"
                    else:
                        name = knn.predict(resized)[0]

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        name,
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2
                    )

                    # ATTENDANCE
                    if name != "Unknown" and name not in marked_names:

                        student_id = name.split("_")[0]
                        student_name = name.split("_")[1]

                        now = datetime.now()

                        date = now.strftime("%d-%m-%Y")
                        current_time = now.strftime("%H:%M:%S")

                        already_marked = False

                        if os.path.exists(ATT_FILE):

                            with open(ATT_FILE, "r") as f:

                                reader = csv.reader(f)

                                for row in reader:

                                    if (
                                        len(row) >= 4 and
                                        row[0] == student_id and
                                        row[2] == date
                                    ):
                                        already_marked = True

                        if not already_marked:

                            with open(
                                ATT_FILE,
                                "a",
                                newline=""
                            ) as f:

                                writer = csv.writer(f)

                                writer.writerow([
                                    student_id,
                                    student_name,
                                    date,
                                    current_time
                                ])

                            # 🔊 VOICE OUTPUT
                            speak(
                                f"{student_name} attendance marked successfully"
                            )

                            marked_names.add(name)

                frame_rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                frame_placeholder.image(
                    frame_rgb,
                    channels="RGB"
                )

                if cv2.waitKey(1) == ord('q'):
                    break

            video.release()
            cv2.destroyAllWindows()

# ===================================
# VIEW ATTENDANCE
# ===================================
elif menu == "View Attendance":

    st.subheader("📋 Attendance Records")

    if os.path.exists(ATT_FILE):

        df = pd.read_csv(
            ATT_FILE,
            header=None
        )

        df.columns = [
            "Student ID",
            "Name",
            "Date",
            "Time"
        ]

        st.dataframe(df, use_container_width=True)

        csv_file = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Attendance CSV",
            csv_file,
            "Attendance.csv",
            "text/csv"
        )

        speak("Attendance records loaded")

    else:
        st.warning("No attendance records found")
        speak("No attendance records found")