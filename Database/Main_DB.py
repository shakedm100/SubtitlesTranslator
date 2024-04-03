import sqlite3
from datetime import datetime

import config

db_path = config.directory
def initialize_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS letter_count (date TEXT PRIMARY KEY, count INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS directory (name TEXT PRIMARY KEY, value TEXT)''')

    conn.commit()
    conn.close()


initialize_db()

def update_letter_count(letter_count):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #Today's date in MM-YYYY format
    today = datetime.now().strftime('%m-%Y')

    c.execute('INSERT OR REPLACE INTO letter_count (date, count) VALUES (?, COALESCE((SELECT count FROM letter_count WHERE date = ?), 0) + ?)',
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

def set_main_directory(directory_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Update the main directory location in the settings table
    c.execute('INSERT OR REPLACE INTO directory (name, value) VALUES (?, ?)',
              ('main_directory', directory_path))

    conn.commit()
    conn.close()

def get_main_directory():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT value FROM directory WHERE name = "main_directory"')
    row = c.fetchone()

    conn.close()
    return row[0] if row else None