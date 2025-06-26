import streamlit as st
import cv2
import easyocr
import torch
import pandas as pd
import os
from datetime import datetime
from database import init_db, verify_guard, save_detection, get_logs

# ---------------------------------------------
# 🔁 INIT DB
init_db()

# ---------------------------------------------
# 🔐 Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def login():
    st.title("🔐 LicenseLog - Guard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_guard(username, password):
            st.success(f"Welcome, {username} 👮")
            st.session_state.logged_in = True
            st.session_state.current_user = username
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully.")

# ---------------------------------------------
# 🚪 Redirect to login if not authenticated
if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------------------------------------
# 👮 Logged-in UI starts here
st.title("🚗 LicenseLog - ALPR Dashboard")

# Sidebar for logout
st.sidebar.title("👮 Security Panel")
st.sidebar.write(f"Logged in as: `{st.session_state.current_user}`")
if st.sidebar.button("Logout"):
    logout()
    st.stop()

# ---------------------------------------------
# Load YOLOv5 model and EasyOCR
model = torch.hub.load('yolov5', 'custom', path='weights/best.pt', source='local')
reader = easyocr.Reader(['en'])

def process_frame(frame):
    results = model(frame)
    df = results.pandas().xyxy[0]
    plates = []

    for _, row in df.iterrows():
        xmin, ymin, xmax, ymax = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
        conf = float(row['confidence']) * 100
        roi = frame[ymin:ymax, xmin:xmax]
        ocr_result = reader.readtext(roi)
        text = ocr_result[0][1] if ocr_result else "N/A"

        # Save to database
        save_detection(text, conf, st.session_state.current_user)

        # Draw
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(frame, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

        plates.append(text)

    return frame, plates

# ---------------------------------------------
# Webcam Feed
run = st.checkbox('Start Webcam')
FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        processed_frame, _ = process_frame(frame)
        FRAME_WINDOW.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))

    cap.release()

# ---------------------------------------------
# Detection Logs
st.subheader("📊 Detection Logs")
logs = get_logs()
df_logs = pd.DataFrame(logs, columns=["ID", "Timestamp", "Plate", "Confidence", "Guard"])
st.dataframe(df_logs)
