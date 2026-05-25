# csc131-project
Group project for CSC 131 at Sac State

The Intake Automation Prototype is designed to streamline the process of collecting and organizing student registration data for a CPR training business. Currently, the client must manually review multiple sources of information, including registration emails, payment confirmations, and instructor platform data. This process is repetitive, time-consuming, and increases the likelihood of missed, duplicated, or inconsistent records.

The purpose of this system is to automate key parts of that workflow by retrieving relevant data, extracting student information, and presenting it in a centralized dashboard. The system allows the user to view, search, filter, and manage student records more efficiently, while also supporting export functionality for reporting or external use.

## Setup

To install dependencies and run the app, execute the following commands in the terminal.

1. Install dependencies:
    pip install -r requirements.txt

2. Run the app:
python -m streamlit run app/main.py

## Demo Instructions

Once the run command is entered, the Streamlit UI should open in the local browser. From there, the user can navigate between the different pages using the navigation menu. 

The application includes pages for the dashboard intake records, student details, export options, and email automation. The automation scraper can be accessed from the navigation menu. Running the automation process may require the user to sign into the applicable email account, especially during first time setup.

## Known Issues and Limitiations.

Currently, the program runs locally through Streamlit on localhost. Given the project timeline and lack of monetary resources allocated to deployment, we did not fully explore cloud hosting or production deployment options. As a result, the app is best understood as a working prototype rather than a fully deployed client-ready system.

The automation process may also depend on account permissions, authentication settings, email access, and network restrictions. These factors can affect whether the program is able to successfully connect to outside services during testing.

Additionally, some features are still limited by the prototype stage of development. The system demonstrates the intended workflow, user interface, and automation concept, but further work would be needed to improve error handling, deployment, security, and long-term maintainability.
