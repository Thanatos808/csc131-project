# Student Class Registration Scheduler
## Overview
Our scheduler is a student class registration scheduler made using Python and Tkinter. The goal was to create a user friendly scheduler similar to the client’s Acuity style scheduler, where students can easily register for classes, select available time slots, view locations, and manage registrations through an interactive calendar system.

The program saves registrations into a JSON file so the data stays saved after the program closes.

## Tools and Libraries
- Python,Tkinter,JSON
## How to Run
cd scheduler_gui
python gui.py
## Files
gui.py
Handles the GUI and calendar.
scheduler_core.py
Handles registration logic and saving data.
appointment.py 
Stores appointment information.
appointments.json
Stores saved registrations.
