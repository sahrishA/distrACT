from models import get_connection


def get_or_create_student(name, email):
    """Return the StudentID for this email, creating the student if needed."""
    connection = get_connection()

    row = connection.execute(
        "SELECT StudentID FROM Students WHERE Email = ?",
        (email,),
    ).fetchone()

    if row:
        student_id = row["StudentID"]
    else:
        cursor = connection.execute(
            "INSERT INTO Students (Name, Email) VALUES (?, ?)",
            (name, email),
        )
        student_id = cursor.lastrowid
        connection.commit()

    connection.close()

    return student_id


def create_activity(
    student_id,
    title,
    date,
    start_time,
    end_time,
    description=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO Activities
    (StudentID, Title, Description, Date, StartTime, EndTime)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        title,
        description,
        date,
        start_time,
        end_time
    ))

    activity_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return activity_id


def get_student_activities(student_id):
    connection = get_connection()

    activities = connection.execute("""
    SELECT
        ActivityID,
        Title,
        Description,
        Date,
        StartTime,
        EndTime
    FROM Activities
    WHERE StudentID = ?
    ORDER BY Date, StartTime
    """, (student_id,)).fetchall()

    connection.close()

    return activities
