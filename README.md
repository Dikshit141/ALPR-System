# 🚗 LicenseLog - ALPR System

A real-time **Automatic License Plate Recognition** (ALPR) system built for **college security guards**, using:

* YOLOv5 for object detection
* EasyOCR for plate number recognition
* Streamlit for the UI
* SQLite + bcrypt for secure login and log management

---

## 📸 Features

* 🔍 Real-time license plate detection using a trained YOLOv5 model
* 🧠 EasyOCR extracts plate numbers from detected ROIs
* 👮‍♂️ Guard login/logout system (stored in SQLite, passwords hashed)
* 📦 Detection logs are saved with timestamps, confidence, and detected guard
* 🧾 Full dashboard in Streamlit, no browser extension or CLI needed

---

## 📊 Tech Stack

| Component   | Technology      |
| ----------- | --------------- |
| UI          | Streamlit       |
| Detection   | YOLOv5          |
| OCR         | EasyOCR         |
| Auth + Logs | SQLite + bcrypt |
| Language    | Python          |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/LicenseLog-ALPR.git
cd LicenseLog-ALPR
```

### 2. Create and activate virtual environment

```bash
python -m venv alpr-env
# Windows:
./alpr-env/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:

```bash
pip install streamlit opencv-python easyocr torch pandas bcrypt
```

### 4. Add trained model

Download the trained model from:

👉 [Download best.pt](https://drive.google.com/file/d/1gewNNTHYEZtJqU4AUkGfjPdDKYGhh2hG/view?usp=sharing)

Then place it here:

```
LicenseLog-ALPR/
└── weights/
    └── best.pt
```

---

## 🔐 Register Guard

Run this script once to add a guard to the database:

```python
# register_guard.py
from database import register_guard
register_guard("guard1", "1234")
```

Login credentials will be:

* Username: `guard1`
* Password: `1234`

Passwords are stored securely using bcrypt.

---

## ▶️ Run the App

```bash
streamlit run dashboard.py
```

* Login as a registered guard
* Click **Start Webcam** to begin detection
* View logs in the dashboard

---

## 📊 Detection Logs Table

| ID | Timestamp           | Plate No   | Confidence | Detected By |
| -- | ------------------- | ---------- | ---------- | ----------- |
| 1  | 2025-06-25 19:43:12 | MH12AB1234 | 91.3       | guard1      |

Saved in `alpr.db` (SQLite).

---

## 🧱 Folder Structure

```
LicenseLog-ALPR/
├── dashboard.py           # Streamlit dashboard
├── database.py            # Auth + logging database logic
├── register_guard.py      # Script to add guard credentials
├── alpr.db                # SQLite database (auto-generated)
├── weights/
│   └── best.pt            # YOLOv5 trained model (optional)
├── requirements.txt       # Python dependencies
├── .gitignore             # Files to ignore on GitHub
└── README.md
```

---

## 🚫 Files Not Pushed to GitHub

Your `.gitignore` file should exclude:

```
__pycache__/
alpr-env/
alpr.db
alpr_log.csv
data/
weights/*.pt
```

---

## 💡 Potential Enhancements

* [ ] Admin panel to manage guards and logs
* [ ] Export logs to Excel or PDF
* [ ] Upload image for offline detection
* [ ] Plate blacklist alerts
* [ ] Host on Streamlit Cloud or Hugging Face

---

## 📚 References

* [YOLOv5](https://github.com/ultralytics/yolov5)
* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [Streamlit](https://streamlit.io/)

---

## 👨‍💻 Author

**Dikshit**
M.Tech CSE, Thapar University
📧 [dikshitkapoor03@gmail.com](mailto:dikshitkapoor03@gmail.com)

---

## 🛡️ License

This project is for educational and demo purposes. Contact the author for deployment permissions.
