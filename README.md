# Overview

As a software engineer, I developed this Student Records Management System to deepen my understanding of relational databases and full-stack application development. The software is a comprehensive Python application that integrates with an SQLite relational database to manage student information and attendance records. It provides both a command-line interface for direct interaction and a web-based GUI built with Streamlit, allowing users to perform CRUD operations, execute JOIN queries, calculate aggregates, and filter data by dates.

To use the program, run the CLI with `python student_records.py` for interactive menus, or launch the web GUI with `streamlit run app.py` for a browser-based interface. The CLI offers options to add, view, update, and delete students and attendance, view joined data, get summaries, and filter by dates. The web app provides intuitive pages for students, attendance, reports, and seeding data.

My purpose in writing this software was to advance my skills in database design, SQL query construction, and integrating databases with Python applications, while building a practical tool that demonstrates real-world database operations.

[Software Demo Video](https://youtu.be/XWLny7JhmW0)

# Relational Database

The relational database used is SQLite, a lightweight, file-based SQL database engine that is built into Python, making it ideal for development and small-scale applications without requiring a separate database server.

The database consists of two main tables:

- **Students Table**: Stores student information with columns for id (primary key, auto-increment), name (text, not null), and grade (real number).
- **Attendance Table**: Tracks attendance records with columns for id (primary key, auto-increment), student_id (foreign key referencing students.id), date (text in ISO format YYYY-MM-DD), and status (text, e.g., 'Present' or 'Absent').

These tables are linked via a foreign key relationship, enabling JOIN operations to combine student data with their attendance history.

# Development Environment

I used Visual Studio Code as my primary code editor for writing and debugging the Python code. The development environment included Python 3.x as the programming language, with the built-in sqlite3 module for database operations. For the web GUI, I utilized Streamlit as the framework, along with pandas for data manipulation and display in tabular formats.

# Useful Websites

- [Python Official Documentation](https://docs.python.org/3/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

# Future Work

- Implement user authentication and role-based permissions for secure access
- Add data export/import functionality (CSV, JSON formats)
- Add email notifications for attendance alerts
- Implement data backup and recovery features