import streamlit as st

def renderTopSummary(totalRecords=0, backlog=0, inProgress=0, completed=0):
    st.markdown("## CSC 131 - Automation Prototype")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", totalRecords)
    col2.metric("Backlog", backlog)
    col3.metric("In Progress", inProgress)
    col4.metric("Completed", completed)

    st.divider()

def renderStatusCards():
    leftCol, rightCol = st.columns(2)

    with leftCol:
        st.markdown("### Workflow")
        st.markdown(
             """
1. **Intake** — Add a new student record  
2. **Dashboard** — Review and filter records  
3. **Student Detail** — View an individual record  
4. **Export** — Download structured data
            """
        )

        st.markdown("### Getting Started")
        st.markdown(
            """
- Navigate to **Intake** to create a student record  
- Use **Dashboard** to view and search records  
- Open **Student Detail** for full record information  
- Export data from the **Export** page
            """
        )

    with rightCol:
        st.markdown("### Session Status")

        hasRecords = len(st.session_state.get("studentRecords", [])) > 0
        sheetsConfigured = st.session_state.get("googleSheetsConfigured", False)

        if hasRecords:
            st.success("Student records are loaded in this session.")
        else:
            st.info("No student records in this session yet.")

        if sheetsConfigured:
            st.success("Google Sheets integration is configured.")
        else:
            st.warning("Google Sheets target not configured.")

        st.markdown("### Navigation")
        st.markdown(
            """
Use the sidebar to access:

- Home  
- Dashboard  
- Intake  
- Student Detail  
- Export
            """
        )

def renderBottomNav():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Go to Intake", use_container_width=True):
            st.switch_page("pages/Intake.py")

    with col2:
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("pages/Dashboard.py")

    with col3:
        if st.button("Go to Export", use_container_width=True):
            st.switch_page("pages/Export.py")