# database.py
import sqlite3
import hashlib
import secrets
from datetime import datetime

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('hostel.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def initialize_database():
    """Initialize the database with tables and sample data"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT UNIQUE NOT NULL,
                           password TEXT NOT NULL,
                           email TEXT UNIQUE NOT NULL,
                           room_number TEXT,
                           phone TEXT,
                           registered_on TEXT)''')
            
            # Create outpass table
            cursor.execute('''CREATE TABLE IF NOT EXISTS outpasses
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER,
                           reason TEXT,
                           departure_date TEXT,
                           return_date TEXT,
                           status TEXT DEFAULT 'pending',
                           FOREIGN KEY(user_id) REFERENCES users(id))''')
            
            # Insert sample data if tables are empty
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
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

def hash_password(password):
    """Securely hash a password with salt using SHA-256"""
    salt = secrets.token_hex(16)  # Generate a random salt
    salted_password = salt + password
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return f"{salt}${hashed}"  # Store salt and hash together

def verify_password(plain_password, hashed_password):
    """Verify a password against its hashed version"""
    if not hashed_password or '$' not in hashed_password:
        return False
    salt, stored_hash = hashed_password.split('$')
    salted_password = salt + plain_password
    computed_hash = hashlib.sha256(salted_password.encode()).hexdigest()
    return computed_hash == stored_hash

if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully")
