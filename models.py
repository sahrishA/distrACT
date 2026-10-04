import sqlite3


def get_connection():
    connection = sqlite3.connect("focussync.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE
    )
    """)

    # Activity table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Activities (
        ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        Title TEXT NOT NULL,
        Description TEXT,
        Date TEXT NOT NULL,
        StartTime TEXT NOT NULL,
        EndTime TEXT NOT NULL,
        FOREIGN KEY (StudentID)
            REFERENCES Students(StudentID)
    )
    """)

    # Add Description to Activities tables created before it existed
    columns = [
        row["name"]
        for row in cursor.execute("PRAGMA table_info(Activities)")
    ]
    if "Description" not in columns:
        cursor.execute("ALTER TABLE Activities ADD COLUMN Description TEXT")

    connection.commit()
    connection.close()