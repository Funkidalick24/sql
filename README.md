# Student Records Management System

A Python-based Student Records Management System using SQLite for relational database management. This system demonstrates full CRUD operations, JOIN queries, aggregate functions, and date-based filtering as part of the CSE 310 Applied Programming module on SQL Relational Databases.

## Features

- **Student Management**: Add, view, update, and delete student records (name and grade).
- **Attendance Tracking**: Record and manage attendance for students with dates and status.
- **JOIN Queries**: View students along with their attendance records.
- **Aggregate Functions**: Summarize attendance counts and calculate average grades.
- **Date Filtering**: Filter attendance records by date ranges.
- **Command-Line Interface**: Interactive CLI for all operations.
- **Demo Mode**: Run a demonstration of all features without user input.

## Requirements

- Python 3.x
- SQLite (built-in with Python)

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install dependencies (if any):

```bash
pip install -r requirements.txt
```

3. Download or clone the repository containing `student_records.py`.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Download or clone the repository containing `student_records.py`.

## Usage

### Running the Interactive CLI

```bash
python student_records.py
```

This launches the command-line interface where you can:
- Add/view/update/delete students
- Add/view/update/delete attendance records
- View joined student-attendance data
- Get attendance summaries and average grades
- Filter attendance by date ranges
- Seed example data

### Running the Demo

```bash
python student_records.py demo
```

This runs a complete demonstration of the system, seeding data and displaying all features.

### Running the Web GUI (Streamlit)

```bash
streamlit run app.py
```

This launches a web-based graphical user interface in your browser with:
- **Students Page**: Manage student records (add, view, update, delete)
- **Attendance Page**: Manage attendance records with student selection
- **Reports Page**: View summaries, joined data, and date-filtered reports
- **Seed Data Page**: Add example data for testing

The web app provides a modern, user-friendly interface while using the same underlying database and functions.

## Database Schema

### Students Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL)
- `grade` (REAL)

### Attendance Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `student_id` (INTEGER NOT NULL, FOREIGN KEY to students.id)
- `date` (TEXT NOT NULL, ISO format YYYY-MM-DD)
- `status` (TEXT NOT NULL, e.g., 'Present', 'Absent')

## Module Requirements Met

- **Relational Database**: Uses SQLite with proper table relationships.
- **CRUD Operations**: Full create, read, update, delete for both tables.
- **SQL Queries**: Programmatically builds and executes queries in Python.
- **JOINs**: Demonstrates LEFT JOIN between students and attendance.
- **Aggregates**: Uses COUNT and AVG functions for summaries.
- **Date Handling**: Stores dates in ISO format and filters by date ranges.
- **Example Data**: Includes seeded data to showcase functionality.
- **Extensibility**: Designed for future GUI or web interface integration.

## Development Schedule

The system was developed over two weeks following a structured sprint plan:

### Week 1
- Research relational databases and Python-SQLite integration
- Plan database schema and program structure
- Set up environment and create tables
- Implement student CRUD operations
- Implement attendance functionality

### Week 2
- Test CRUD operations
- Implement JOIN queries and aggregates
- Add date-based filtering
- Integrate full workflow
- Seed data and create CLI demo
- Debug and refine

## Risks and Mitigation

1. **Limited SQL Experience**: Mitigated through tutorials, isolated testing, and seeking help.
2. **Debugging Integration**: Used parameterized queries, individual testing, and code comments.
3. **Time Management**: Followed strict schedule, broke tasks into daily steps, tracked progress.

## Future Enhancements

- Web-based GUI using Flask or Django
- Mobile app interface
- Advanced reporting and analytics
- User authentication and permissions
- Data export/import functionality