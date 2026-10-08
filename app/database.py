import sqlite3
from pathlib import Path


DATABASE_PATH = Path("certificates.db")


def get_db():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()


def init_db():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            organization TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'queued',
            total INTEGER DEFAULT 0,
            successful INTEGER DEFAULT 0,
            failed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            recipient_name TEXT NOT NULL,
            recipient_email TEXT NOT NULL,
            course TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            file_path TEXT,
            error_message TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    connection.commit()
    connection.close()