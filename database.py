import sqlite3
import bcrypt
from datetime import datetime

# Initialize database with sample credentials
def init_db():
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 room_number TEXT,
                 phone TEXT,
                 registered_on TEXT)''')
    
    # Create outpass table
    c.execute('''CREATE TABLE IF NOT EXISTS outpasses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 reason TEXT,
                 departure_date TEXT,
                 return_date TEXT,
                 status TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Insert sample users if they don't exist
    sample_users = [
        ('admin', hash_password('admin123'), 'admin@hostel.com', 'A101', '9876543210'),
        ('student1', hash_password('student123'), 'student1@hostel.com', 'B202', '8765432109'),
        ('student2', hash_password('student123'), 'student2@hostel.com', 'C303', '7654321098')
    ]
    
    for user in sample_users:
        try:
            c.execute("INSERT INTO users (username, password, email, room_number, phone, registered_on) VALUES (?, ?, ?, ?, ?, ?)",
                     (*user, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except sqlite3.IntegrityError:
            pass  # User already exists
    
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))