import streamlit as st
from datetime import datetime


def renderIntake():
    st.title("Intake")

   
    if "students" not in st.session_state:
        st.session_state["students"] = []

    with st.form("intake_form"):
        student_name = st.text_input("Student Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        course = st.text_input("Course")
        class_date = st.text_input("Class Date")
        location = st.text_input("Location")

        submitted = st.form_submit_button("Add Student")

    if submitted:
        new_student = {
            "student_name": student_name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "course": course.strip(),
            "class_date": class_date.strip(),
            "location": location.strip(),
            "received_datetime": datetime.now().isoformat(timespec="seconds"),
        }

        st.session_state["students"].append(new_student)
        st.success("Student added!")

    
    if st.session_state["students"]:
        st.subheader("Students collected so far")
        st.dataframe(st.session_state["students"], use_container_width=True)
    else:
        st.info("No students added yet.")
