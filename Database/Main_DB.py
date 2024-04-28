import logging
import sqlite3
from datetime import datetime

import config

db_path = config.directory


def initialize_db():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS letter_count (date TEXT PRIMARY KEY, count INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS directories (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT)''')

        conn.commit()
        conn.close()

        logging.info("Initialized DB")
    except:
        logging.info("Failed to initialize DB")


initialize_db()


def update_letter_count(letter_count):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Today's date in MM-YYYY format
    today = datetime.now().strftime('%m-%Y')

    c.execute(
        'INSERT OR REPLACE INTO letter_count (date, count) VALUES (?, COALESCE((SELECT count FROM letter_count WHERE date = ?), 0) + ?)',
        (today, today, letter_count))

    conn.commit()
    conn.close()


def get_latest_letter_count():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT count FROM letter_count ORDER BY date DESC LIMIT 1")
    letters = c.fetchone()
    conn.close()

    return letters[0] if letters else None


def set_directories(directory_array):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for directory in directory_array:
        # Check if the path already exists
        cursor.execute('SELECT id FROM directories WHERE path = ?', (directory,))
        if cursor.fetchone() is None:
            # If the path does not exist, insert it
            cursor.execute('INSERT INTO directories (path) VALUES (?);', (directory,))
            print("Path inserted.")
        else:
            print("Path already exists.")

    conn.commit()
    conn.close()


def get_directories():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT path FROM directories')
    all_paths = [row[0] for row in c.fetchall()]  # Extract path values into a list

    conn.close()
    return all_paths
