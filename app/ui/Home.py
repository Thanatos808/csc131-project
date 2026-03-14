import streamlit as st

def renderHome():
    students = st.session_state.get("students", [])

    totalRecords = len(students)
    backlog = len([s for s in students if s.get("status", "Backlog") == "Backlog"])
    inProgress = len([s for s in students if s.get("status") == "In Progress"])
    completed = len([s for s in students if s.get ("status") == "Completed"])

    st.title("CSC 131 - Automation Prototype")
    
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", totalRecords)

    with col2:
        st.metric("Backlog", backlog)

    with col3:
        st.metric("In Progress", inProgress)

    with col4:
        st.metric("Completed", completed)

    st.divider()

    leftCol, rightCol = st.columns([1.4, 1])

    with leftCol:
        with st.container(border=True):
            st.subheader("Workflow")
            st.markdown(
                """
                1. **Intake** — Add a new student record  
                2. **Dashboard** — Review and filter records  
                3. **Student Detail** — View an individual record  
                4. **Export** — Download structured data
                """
            )
        
        with st.container(border=True):
            st.subheader("Getting Started")
            st.markdown(
                """
                - Navigate to **Intake** to create a student record  
                - Use **Dashboard** to view and search records  
                - Open **Student Detail** for full record information  
                - Export data from the **Export** page
                """
            )

        with rightCol:
            with st.container(border=True):
                st.subheader("Session Status")

                if totalRecords > 0:
                    st.success("Student records are loaded in the session.")
                else:
                    st.info("No student records in the session yet.")

                sheetID = st.session_state.get("sheet_id", "").strip()

                if sheetID:
                    st.success("Google Sheets target configured.")
                else:
                    st.warning("Googlee Sheets target not configured.")

            with st.container(border=True):
                st.subheader("Navigation")
                st.write("Use the sidebar to access:")
                st.markdown(
                    """
                    - Home  
                    - Dashboard  
                    - Intake  
                    - Student Detail  
                    - Export
                    """
                )

        st.divider()

    nav1, nav2, nav3 = st.columns(3)

    with nav1:
        if st.button("Go to Intake", use_container_width=True):
            st.session_state["currentPage"] = "Intake"
            st.rerun()

    with nav2:
        if st.button("Go to Dashboard", use_container_width=True):
            st.session_state["currentPage"] = "Dashboard"
            st.rerun()

    with nav3:
        if st.button("Go to Export", use_container_width=True):
            st.session_state["currentPage"] = "Export"
            st.rerun()
                