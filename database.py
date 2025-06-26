import sqlite3
import bcrypt
from datetime import datetime

DB_PATH = "alpr.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Guards table
    c.execute('''CREATE TABLE IF NOT EXISTS guards (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')

    # Detection logs
    c.execute('''CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        license_plate TEXT,
        confidence REAL,
        detected_by TEXT
    )''')
    conn.commit()
    conn.close()

def register_guard(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO guards (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()

def verify_guard(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM guards WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row and bcrypt.checkpw(password.encode(), row[0])

def save_detection(plate, confidence, guard):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO detections (timestamp, license_plate, confidence, detected_by) VALUES (?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), plate, confidence, guard))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM detections ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
