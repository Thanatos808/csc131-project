import streamlit as st
import pandas as pd

def renderDashboard():
    st.title("Dashboard")
    
    #Filter Section

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        #dropdown to filter by status
        statusFilter = st.selectbox(
            "Status",
            ["All", "Backlog", "In Progress", "Completed"]
        )

    with col2:
        #text search input
        searchText = st.text_input("Search (name or email)")

    with col3:
        #placeholder button for future use
        st.write("")
        st.write("")
        st.button("Refresh")
        
    st.divider()

        #Temporary Dummy Data
        #Replace later with loadStudents()

    data= [
        {"recordId": "R-1001", "Name": "John Smith", "Email": "john@example.com", "Course": "BLS", "Status": "Backlog"},
        {"recordId": "R-1002", "Name": "Sarah Lee", "Email": "sarah@example.com", "Course": "ACLS", "Status": "In Progress"},
        {"recordId": "R-1003", "Name": "Mike Davis", "Email": "mike@example.com", "Course": "PALS", "Status": "Completed"},
    ]

    df = pd.DataFrame(data)

    #Apply Filtering Logic

    if statusFilter != "All":
        df = df[df["Status"] == statusFilter]

    if searchText.strip():
        q = searchText.strip()
        df = df[
            df["Name"].str.contains(q, case=False)
            | df["Email"].str.contains(q, case=False)
        ]

    #Display table

    if df.empty:
        st.info("No records found.")
        return
    
    #Show only visible columns
    st.dataframe(
        df[["Name," "Email", "Course", "Status"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Open Record")

    #Create readable labels for dropdown
    recordLabels = [
        f'{row["Name"]} ({row["Email"]})'
        for _, row in df.iterows()
    ]   

    selectedLabel = st.selectbox("Select a student", recordLabels)

    #Find selected row
    selectedRow = df.iloc[recordLabels.index(selectedLabel)]

    #When button clicked
    # 1. save selected record ID
    # 2. switch page to Student Detail
    # 3. Rerun app so navigation updates immediately
    if st.button("Open Student Detail", type="primary"):
        st.session_state["selectedRecordId"] = selectedRow["recordId"]
        st.session_state["currentPage"] = "Student Detail"
        st.rerun()