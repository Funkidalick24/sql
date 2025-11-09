import streamlit as st
import pandas as pd
from student_records import (
    create_tables, add_student, get_students, update_student, delete_student,
    add_attendance, get_attendance, update_attendance, delete_attendance,
    get_students_with_attendance, get_attendance_summary, get_average_grade,
    get_attendance_by_date_range, seed_data
)

# Initialize database
create_tables()

# Page configuration
st.set_page_config(page_title="Student Records Management", page_icon="📚", layout="wide")

# Title
st.title("📚 Student Records Management System")

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["Students", "Attendance", "Reports", "Seed Data"])

if page == "Students":
    st.header("👨‍🎓 Student Management")

    # Display current students
    st.subheader("Current Students")
    students = get_students()
    if students:
        df_students = pd.DataFrame(students, columns=["ID", "Name", "Grade"])
        st.dataframe(df_students, use_container_width=True)
    else:
        st.info("No students found. Add some below!")

    # Add new student
    st.subheader("Add New Student")
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        grade = st.number_input("Grade", min_value=0.0, max_value=100.0, step=0.1)
        submitted = st.form_submit_button("Add Student")
        if submitted and name:
            add_student(name, grade)
            st.success(f"Student '{name}' added successfully!")
            st.rerun()

    # Update student
    st.subheader("Update Student")
    if students:
        student_options = {f"{s[0]} - {s[1]}": s[0] for s in students}
        selected_student = st.selectbox("Select Student to Update", list(student_options.keys()))
        if selected_student:
            student_id = student_options[selected_student]
            with st.form(f"update_student_form_{student_id}"):
                new_name = st.text_input("New Name", value=next(s[1] for s in students if s[0] == student_id))
                new_grade = st.number_input("New Grade", value=float(next(s[2] for s in students if s[0] == student_id)),
                                          min_value=0.0, max_value=100.0, step=0.1)
                update_submitted = st.form_submit_button("Update Student")
                if update_submitted:
                    update_student(student_id, new_name, new_grade)
                    st.success("Student updated successfully!")
                    st.rerun()

    # Delete student
    st.subheader("Delete Student")
    if students:
        delete_options = {f"{s[0]} - {s[1]}": s[0] for s in students}
        selected_delete = st.selectbox("Select Student to Delete", list(delete_options.keys()))
        if selected_delete and st.button("Delete Student"):
            delete_student(delete_options[selected_delete])
            st.success("Student deleted successfully!")
            st.rerun()

elif page == "Attendance":
    st.header("📅 Attendance Management")

    # Display current attendance
    st.subheader("Current Attendance Records")
    attendance = get_attendance()
    if attendance:
        df_attendance = pd.DataFrame(attendance, columns=["ID", "Student ID", "Date", "Status"])
        st.dataframe(df_attendance, use_container_width=True)
    else:
        st.info("No attendance records found. Add some below!")

    # Get students for dropdown
    students = get_students()
    if not students:
        st.warning("Please add students first before managing attendance.")
    else:
        student_options = {f"{s[0]} - {s[1]}": s[0] for s in students}

        # Add attendance
        st.subheader("Add Attendance Record")
        with st.form("add_attendance_form"):
            selected_student = st.selectbox("Select Student", list(student_options.keys()))
            date = st.date_input("Date")
            status = st.selectbox("Status", ["Present", "Absent"])
            add_submitted = st.form_submit_button("Add Attendance")
            if add_submitted and selected_student:
                student_id = student_options[selected_student]
                add_attendance(student_id, str(date), status)
                st.success("Attendance record added successfully!")
                st.rerun()

        # Update attendance
        st.subheader("Update Attendance Record")
        if attendance:
            attendance_options = {f"ID {a[0]} - Student {a[1]} - {a[2]} ({a[3]})": a[0] for a in attendance}
            selected_attendance = st.selectbox("Select Attendance to Update", list(attendance_options.keys()))
            if selected_attendance:
                attendance_id = attendance_options[selected_attendance]
                with st.form(f"update_attendance_form_{attendance_id}"):
                    new_status = st.selectbox("New Status", ["Present", "Absent"])
                    update_submitted = st.form_submit_button("Update Attendance")
                    if update_submitted:
                        update_attendance(attendance_id, new_status)
                        st.success("Attendance updated successfully!")
                        st.rerun()

        # Delete attendance
        st.subheader("Delete Attendance Record")
        if attendance:
            delete_options = {f"ID {a[0]} - Student {a[1]} - {a[2]} ({a[3]})": a[0] for a in attendance}
            selected_delete = st.selectbox("Select Attendance to Delete", list(delete_options.keys()))
            if selected_delete and st.button("Delete Attendance"):
                delete_attendance(delete_options[selected_delete])
                st.success("Attendance record deleted successfully!")
                st.rerun()

elif page == "Reports":
    st.header("📊 Reports & Summaries")

    # Students with attendance
    st.subheader("Students with Attendance Records")
    joined_data = get_students_with_attendance()
    if joined_data:
        df_joined = pd.DataFrame(joined_data, columns=["Student ID", "Name", "Grade", "Date", "Status"])
        st.dataframe(df_joined, use_container_width=True)
    else:
        st.info("No joined data available.")

    # Attendance summary
    st.subheader("Attendance Summary")
    summary = get_attendance_summary()
    if summary:
        df_summary = pd.DataFrame(summary, columns=["Status", "Count"])
        st.bar_chart(df_summary.set_index("Status"))
        st.dataframe(df_summary, use_container_width=True)
    else:
        st.info("No attendance summary available.")

    # Average grade
    st.subheader("Average Grade")
    avg_grade = get_average_grade()
    if avg_grade:
        st.metric("Average Student Grade", f"{avg_grade:.2f}")
    else:
        st.info("No grades available.")

    # Date range filter
    st.subheader("Filter Attendance by Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    if st.button("Filter"):
        filtered = get_attendance_by_date_range(str(start_date), str(end_date))
        if filtered:
            df_filtered = pd.DataFrame(filtered, columns=["ID", "Student ID", "Date", "Status"])
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.info("No records found in the selected date range.")

elif page == "Seed Data":
    st.header("🌱 Seed Example Data")
    st.write("Click the button below to add example students and attendance records to the database.")

    if st.button("Seed Data"):
        seed_data()
        st.success("Example data seeded successfully!")
        st.rerun()

    st.info("This will add 3 students and 6 attendance records for demonstration purposes.")