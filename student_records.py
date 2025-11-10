import sqlite3
import os
from datetime import datetime

# Database file
DB_FILE = 'student_records.db'

def create_tables():
    """Create the students and attendance tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade REAL
        )
    ''')

    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_student(name, grade):
    """Add a new student."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, grade) VALUES (?, ?)', (name, grade))
    conn.commit()
    conn.close()

def get_students():
    """Retrieve all students."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def update_student(student_id, name=None, grade=None):
    """Update a student's information."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if name and grade:
        cursor.execute('UPDATE students SET name = ?, grade = ? WHERE id = ?', (name, grade, student_id))
    elif name:
        cursor.execute('UPDATE students SET name = ? WHERE id = ?', (name, student_id))
    elif grade:
        cursor.execute('UPDATE students SET grade = ? WHERE id = ?', (grade, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    """Delete a student and their attendance records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

def add_attendance(student_id, date, status):
    """Add attendance record."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
    conn.commit()
    conn.close()

def get_attendance():
    """Retrieve all attendance records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attendance')
    attendance = cursor.fetchall()
    conn.close()
    return attendance

def update_attendance(attendance_id, status):
    """Update attendance status."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE attendance SET status = ? WHERE id = ?', (status, attendance_id))
    conn.commit()
    conn.close()

def delete_attendance(attendance_id):
    """Delete an attendance record."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance WHERE id = ?', (attendance_id,))
    conn.commit()
    conn.close()

def get_students_with_attendance():
    """JOIN query: Get students with their attendance records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.name, s.grade, a.date, a.status
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        ORDER BY s.id, a.date
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

def get_attendance_summary():
    """Aggregate: Count attendance by status."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) FROM attendance GROUP BY status')
    summary = cursor.fetchall()
    conn.close()
    return summary

def get_average_grade():
    """Aggregate: Average grade of all students."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(grade) FROM students')
    avg = cursor.fetchone()[0]
    conn.close()
    return avg

def get_attendance_by_date_range(start_date, end_date):
    """Filter attendance by date range."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attendance WHERE date BETWEEN ? AND ?', (start_date, end_date))
    records = cursor.fetchall()
    conn.close()
    return records
def get_attendance_by_date(date):
    """Get attendance records for a specific date as a dict of student_id: status."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, status FROM attendance WHERE date = ?', (date,))
    records = cursor.fetchall()
    conn.close()
    return {sid: status for sid, status in records}

def delete_attendance_by_student_date(student_id, date):
    """Delete attendance record for a specific student and date."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance WHERE student_id = ? AND date = ?', (student_id, date))
    conn.commit()
    conn.close()

def seed_data():
    """Add example data."""
    # Add students
    add_student('Alice Johnson', 85.5)
    add_student('Bob Smith', 92.0)
    add_student('Charlie Brown', 78.3)

    # Add attendance
    add_attendance(1, '2023-09-01', 'Present')
    add_attendance(1, '2023-09-02', 'Absent')
    add_attendance(2, '2023-09-01', 'Present')
    add_attendance(2, '2023-09-02', 'Present')
    add_attendance(3, '2023-09-01', 'Absent')
    add_attendance(3, '2023-09-02', 'Present')

def cli_menu():
    """Command-line interface."""
    while True:
        print("\nStudent Records Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Add Attendance")
        print("6. View Attendance")
        print("7. Update Attendance")
        print("8. Delete Attendance")
        print("9. View Students with Attendance")
        print("10. Attendance Summary")
        print("11. Average Grade")
        print("12. Filter Attendance by Date")
        print("13. Seed Example Data")
        print("14. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Name: ")
            grade = float(input("Grade: "))
            add_student(name, grade)
            print("Student added.")
        elif choice == '2':
            students = get_students()
            for s in students:
                print(f"ID: {s[0]}, Name: {s[1]}, Grade: {s[2]}")
        elif choice == '3':
            sid = int(input("Student ID: "))
            name = input("New Name (leave blank to skip): ")
            grade = input("New Grade (leave blank to skip): ")
            grade = float(grade) if grade else None
            update_student(sid, name or None, grade)
            print("Student updated.")
        elif choice == '4':
            sid = int(input("Student ID: "))
            delete_student(sid)
            print("Student deleted.")
        elif choice == '5':
            sid = int(input("Student ID: "))
            date = input("Date (YYYY-MM-DD): ")
            status = input("Status (Present/Absent): ")
            add_attendance(sid, date, status)
            print("Attendance added.")
        elif choice == '6':
            attendance = get_attendance()
            for a in attendance:
                print(f"ID: {a[0]}, Student ID: {a[1]}, Date: {a[2]}, Status: {a[3]}")
        elif choice == '7':
            aid = int(input("Attendance ID: "))
            status = input("New Status: ")
            update_attendance(aid, status)
            print("Attendance updated.")
        elif choice == '8':
            aid = int(input("Attendance ID: "))
            delete_attendance(aid)
            print("Attendance deleted.")
        elif choice == '9':
            results = get_students_with_attendance()
            for r in results:
                print(f"Student ID: {r[0]}, Name: {r[1]}, Grade: {r[2]}, Date: {r[3]}, Status: {r[4]}")
        elif choice == '10':
            summary = get_attendance_summary()
            for s in summary:
                print(f"Status: {s[0]}, Count: {s[1]}")
        elif choice == '11':
            avg = get_average_grade()
            print(f"Average Grade: {avg}")
        elif choice == '12':
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            records = get_attendance_by_date_range(start, end)
            for r in records:
                print(f"ID: {r[0]}, Student ID: {r[1]}, Date: {r[2]}, Status: {r[3]}")
        elif choice == '13':
            seed_data()
            print("Example data seeded.")
        elif choice == '14':
            break
        else:
            print("Invalid choice.")

def demo():
    """Run a demo of the system."""
    print("Running demo...")
    create_tables()
    seed_data()
    print("Seeded data.")

    print("\nStudents:")
    students = get_students()
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}, Grade: {s[2]}")

    print("\nAttendance:")
    attendance = get_attendance()
    for a in attendance:
        print(f"ID: {a[0]}, Student ID: {a[1]}, Date: {a[2]}, Status: {a[3]}")

    print("\nStudents with Attendance:")
    results = get_students_with_attendance()
    for r in results:
        print(f"Student ID: {r[0]}, Name: {r[1]}, Grade: {r[2]}, Date: {r[3]}, Status: {r[4]}")

    print("\nAttendance Summary:")
    summary = get_attendance_summary()
    for s in summary:
        print(f"Status: {s[0]}, Count: {s[1]}")

    print(f"\nAverage Grade: {get_average_grade()}")

    print("\nAttendance from 2023-09-01 to 2023-09-01:")
    records = get_attendance_by_date_range('2023-09-01', '2023-09-01')
    for r in records:
        print(f"ID: {r[0]}, Student ID: {r[1]}, Date: {r[2]}, Status: {r[3]}")

    print("Demo completed.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        create_tables()
        cli_menu()