import sqlite3
import numpy as np
import io
from PIL import Image

DB_PATH = 'faces.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                encoding BLOB NOT NULL,
                image BLOB NOT NULL
            )
        ''')
        conn.commit()

def add_user(name, encoding, image_array):
    encoding_bytes = encoding.astype(np.float32).tobytes()
    img = Image.fromarray(image_array)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO users (name, encoding, image) VALUES (?, ?, ?)',
                  (name, encoding_bytes, img_bytes))
        conn.commit()

def get_all_users():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT name, encoding, image FROM users')
        users = []
        for name, encoding_bytes, img_bytes in c.fetchall():
            encoding = np.frombuffer(encoding_bytes, dtype=np.float32)
            img = Image.open(io.BytesIO(img_bytes))
            img_array = np.array(img)
            users.append({'name': name, 'encoding': encoding, 'image': img_array})
        return users

def get_user(name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT encoding, image FROM users WHERE name=?', (name,))
        row = c.fetchone()
        if row:
            encoding = np.frombuffer(row[0], dtype=np.float32)
            img = Image.open(io.BytesIO(row[1]))
            img_array = np.array(img)
            return {'encoding': encoding, 'image': img_array}
        return None

# Initialize DB on import
initialize_db() 