import streamlit as st
import pandas as pd

def renderDashboard():
    st.title("Dashboard")
    st.caption("Review, search, and open student records.")
    
    #Filter Section
    with st.container(border=True):
        st.subheader("Filters")

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
            st.button("Refresh", use_container_width=True)
        
    st.divider()

    #Temporary Dummy Data
    #Replace later with loadStudents()
    data = [
        {
            "recordId": "R-1001",
            "Name": "John Smith",
            "Email": "john@example.com",
            "Course": "BLS",
            "Class Date": "2026-03-14",
            "AHA Status": "Enrolled",
            "Payment Status": "Paid",
            "Status": "Completed"
        },
        {
            "recordId": "R-1002",
            "Name": "Sarah Lee",
            "Email": "sarah@example.com",
            "Course": "ACLS",
            "Class Date": "2026-03-16",
            "AHA Status": "Pending",
            "Payment Status": "Unpaid",
            "Status": "Backlog"
        },
        {
            "recordId": "R-1003",
            "Name": "Mike Davis",
            "Email": "mike@example.com",
            "Course": "PALS",
            "Class Date": "2026-03-18",
            "AHA Status": "Enrolled",
            "Payment Status": "Pending",
            "Status": "In Progress"
        },
    ]

    df = pd.DataFrame(data)
    totalRecords = len(df)
    backlogCount = len(df[df["Status"] == "Backlog"])
    inProgressCount = len(df[df["Status"] == "In Progress"])
    completedCount = len(df[df["Status"] == "Completed"])

    metricCol1, metricCol2, metricCol3, metricCol4 = st.columns(4)

    with metricCol1:
        st.metric("Total Records", totalRecords)

    with metricCol2:
        st.metric("Backlog", backlogCount)

    with metricCol3:
        st.metric("In Progress", inProgressCount)

    with metricCol4:
        st.metric("Completed", completedCount)
    
    st.divider()

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
    st.subheader("Student Records")
    st.caption("Filtered results are shown below.")

    if df.empty:
        st.info("No records found.")
        return
    
    #Show only visible columns
    with st.container(border=True):
        st.dataframe(
            df[[
                "Name",
                "Email", 
                "Course",
                "Class Date",
                "AHA Status",
                "Payment Status", 
                "Status"
                ]],
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()

    with st.container(border=True):
        st.subheader("Open Record")

        #Create readable labels for dropdown
        recordLabels = [
            f'{row["Name"]} ({row["Email"]})'
            for _, row in df.iterrows()
        ]   

        selectedLabel = st.selectbox("Select a student", recordLabels)

        #Find selected row
        selectedRow = df.iloc[recordLabels.index(selectedLabel)]

        #When button clicked
        # 1. save selected record ID
        # 2. switch page to Student Detail
        # 3. Rerun app so navigation updates immediately
        if st.button("Open Student Detail", type="primary", use_container_width=True):
            st.session_state["selectedRecordId"] = selectedRow["recordId"]
            st.session_state["currentPage"] = "Student Detail"
            st.rerun()