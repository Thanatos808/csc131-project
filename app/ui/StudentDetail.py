import streamlit as st

def renderStudentDetail():
    st.title("Student Detail")
     
    #Retrieve selected record ID from session state
    recordId = st.session_state.get("selectedRecordId", "")

    #If no record selected, show warning
    if not recordId:
        st.warning("No record selected. Go to dashboard and open a record.")
        return

    #for now just confirm correct navigation
    st.success(f"Opened record: {recordId}")
    st.write("Next step: load real record data and allow editing here.")