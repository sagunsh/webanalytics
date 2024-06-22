import sqlite3

from dotenv import load_dotenv
import os

load_dotenv()

filename = os.getenv('DB_FILE', 'analytics.db')
try:
    os.remove(filename)
except:
    pass

conn = None
try:
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        client_id VARCHAR(255) UNIQUE,
        domain VARCHAR(255)
    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS pageview (
            id INTEGER PRIMARY KEY,
            client_id VARCHAR(255),
            url TEXT,
            referrer TEXT,
            source VARCHAR(255),
            ip_addr VARCHAR(255),
            country VARCHAR(255),
            region VARCHAR(255),
            city VARCHAR(255),
            user_agent VARCHAR(500),
            browser VARCHAR(255),
            os VARCHAR(255),
            device VARCHAR(255)
        )''')
    conn.commit()
    print(f'database {filename} created successfully')
except Exception as e:
    print(f'Error creating database: {e}')
finally:
    if conn:
        conn.close()
