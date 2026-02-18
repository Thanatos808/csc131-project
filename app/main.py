import streamlit as st

#import page render functions
from app.ui.Home import renderHome
from app.ui.Dashboard import renderDashboard
from app.ui.Intake import renderIntake
from app.ui.StudentDetail import renderStudentDetail
from app.ui.Export import renderExport

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
    }

    #initialize current page in session state
    #session state allows pages to switch to each other
    if "currentPage" not in st.session_state:
        st.session_state["currentPage"] = "Home"

    #radio button lets user choose page manually
    with st.sidebar:
        st.title("Navigation")
        selectedPage = st.radio("Go to", list(pageOptions.keys()),
        index=(st.session_state["currentPage"])
    )   
    st.session_state["currentPage"] = selectedPage  #update session state with user changes

    pageOptions[selectedPage]()

if __name__== "__main__":
    main()
