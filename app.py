import sqlite3
import hashlib
import secrets
from datetime import datetime

def init_db():
    """Initialize the database with tables and sample data"""
    conn = sqlite3.connect('hostel.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   room_number TEXT,
                   phone TEXT,
                   registered_on TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS outpasses
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   reason TEXT,
                   departure_date TEXT,
                   return_date TEXT,
                   status TEXT DEFAULT 'pending',
                   FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Insert sample data if empty
    if not cursor.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        sample_users = [
            ('admin', hash_password('admin123'), 'admin@hostel.com', 'A101', '9876543210'),
            ('student1', hash_password('student123'), 'student1@hostel.com', 'B202', '8765432109'),
            ('student2', hash_password('student123'), 'student2@hostel.com', 'C303', '7654321098')
        ]
        
        for user in sample_users:
            cursor.execute('''INSERT INTO users 
                           (username, password, email, room_number, phone, registered_on)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                           (*user, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Securely hash password with salt"""
    salt = secrets.token_hex(16)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"

def verify_password(plain_password, hashed_password):
    """Verify password against stored hash"""
    if not hashed_password or '$' not in hashed_password:
        return False
    salt, stored_hash = hashed_password.split('$')
    return hashlib.sha256((salt + plain_password).encode()).hexdigest() == stored_hash
