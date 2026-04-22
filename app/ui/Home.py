import streamlit as st
from ui.CommonWidgets import renderTopSummary, renderStatusCards, renderBottomNav


def renderHome():
    if "studentRecords" not in st.session_state:
        st.session_state["studentRecords"] = []

    if "googleSheetsConfigured" not in st.session_state:
        st.session_state["googleSheetsConfigured"] = False

    def getSummaryCounts():
        records = st.session_state["studentRecords"]

        totalRecords = len(records)
        backlog = sum(1 for record in records if record.get("status", "Backlog") == "Backlog")
        inProgress = sum(1 for record in records if record.get("status") == "In Progress")
        completed = sum(1 for record in records if record.get("status") == "Completed")

        return totalRecords, backlog, inProgress, completed

    totalRecords, backlog, inProgress, completed = getSummaryCounts()

    renderTopSummary(totalRecords, backlog, inProgress, completed)
    renderStatusCards()
    st.divider()
    