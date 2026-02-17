import streamlit as st

from app.ui.Home import renderHome
from app.ui.Dashboard import renderDashboard
from app.ui.Intake import renderIntake
from app.ui.StudentDetail import renderStudentDetail
from app.ui.Export import renderExport

def main():
    st.set_page_config(page_title="CSC 131 Prototype", layout="wide")

    pageOptions= {
        "Home": renderHome,
        "Dashboard": renderDashboard,
        "Intake": renderIntake,
        "Student Detail": renderStudentDetail,
        "Export": renderExport,
    }

    with st.sidebar:
        st.title("Navigation")
        selectedPage = st.radio("Go to", list(pageOptions.keys()), index=0)

    pageOptions[selectedPage]()

if __name__== "__main__":
    main()
