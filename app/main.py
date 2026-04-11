from typing import Dict, List
import streamlit as st

#import page render functions
from ui.Home import renderHome
from ui.Dashboard import renderDashboard
from ui.Intake import renderIntake
from ui.StudentDetail import renderStudentDetail
from ui.Export import renderExport
from ui.EmailAutomation import renderEmailAutomation

def main():
    #configure overall app settings
    st.set_page_config(page_title="CSC 131 Prototype", layout="wide")

    #map page names (sidebar label) to their render function
    pageOptions= {
        "Home": renderHome,
        "Dashboard": renderDashboard,
        "Intake": renderIntake,
        "Student Detail": renderStudentDetail,
        "Export": renderExport,
        "Email Automation": renderEmailAutomation,
    }

    #initialize current page in session state
    #session state allows pages to switch to each other
    if "currentPage" not in st.session_state:
        st.session_state["currentPage"] = "Home"

    #radio button lets user choose page manually
    with st.sidebar:
        st.title("Navigation")
        pageNames = list(pageOptions.keys()) #get list of page names
        currentIndex = pageNames.index(st.session_state["currentPage"]) #find index of current page

        selectedPage = st.radio(
            "Go to",
            pageNames,
            index=currentIndex
        )

        st.session_state["currentPage"] = selectedPage  #update session state with user changes

    pageOptions[selectedPage]()

if __name__ == "__main__":
    main()