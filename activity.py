from models import get_connection


def create_activity(
    student_id,
    title,
    date,
    start_time,
    end_time
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO Activities
    (StudentID, Title, Date, StartTime, EndTime)
    VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        title,
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
        Date,
        StartTime,
        EndTime
    FROM Activities
    WHERE StudentID = ?
    ORDER BY Date, StartTime
    """, (student_id,)).fetchall()

    connection.close()

    return activities