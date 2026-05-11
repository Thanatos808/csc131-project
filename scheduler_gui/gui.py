"""
Quick Description:
This program is a student class registration scheduler.
Students can enter their information, choose a course/location,
select a time slot, and register. The calendar supports date searching,
weekly navigation, canceling registrations, and saving data.
"""
# imports 
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from appointment import Appointment
from scheduler_core import Scheduler
# Setup scheduler
scheduler = Scheduler()
scheduler.load_from_file()
# Main settings
MAX_SEATS = 10
BG = "#fef2f2"
WHITE = "white"
DARK = "#7f1d1d"
RED = "#991b1b"
OPEN = "#fff1f2"
SELECTED = "#fde68a"
# Course and time data
COURSES = ["CPR", "BLS", "ACLS", "PALS"]
TIMES = ["7AM", "8AM", "9AM", "10AM", "11AM", "12PM",
         "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM"]
# Course colors- can be changed 
COURSE_COLORS = {
    "CPR": "#fecaca",
    "BLS": "#fca5a5",
    "ACLS": "#f87171",
    "PALS": "#ef4444"
}
# Locations and addresses from the website 
LOCATIONS = {
    "Atlanta - Chamblee": "2900 Chamblee Tucker Road, Building 11, Suite 100C, Chamblee, GA 30341",
    "Atlanta - Decatur": "3576 Covington Highway, Suite 206, Office B, Decatur, GA 30032",
    "Atlanta - Exchange": "1755 The Exchange, Suite 183, Atlanta GA 30339",
    "Atlanta - Marietta Office": "4180 Providence Rd., Building 200, Suite 210, Marietta, GA 30062",
    "Atlanta - Peachtree Corners": "4047 Holcomb Bridge Rd, Suite 201, Peachtree Corners, GA 30092",
    "Memphis - Bartlett": "3189 Kirby Whitten Road, Suite 203C, Bartlett, TN 38134",
    "Memphis - Perkins": "3885 S. Perkins, Suite 1, Office 19, Memphis, TN 38118",
    "Memphis - Sycamore": "1200 Sycamore View Rd, Suite 205, Memphis TN 38134",
    "Nashville - Brentwood": "1802 Williamson Ct, Suite 100, Brentwood, TN 37027",
    "Nashville - Film House": "810 Dominican Dr., Suite 116A, Nashville, TN 37228",
    "Nashville - Hendersonville": "260 W Main St., Suite 100, Hendersonville, TN 37075",
    "Nashville - Trousdale": "4721 Trousdale Dr. Suite 202, Nashville, TN 37220"
}
# Create window
root = tk.Tk()
root.title("Student Class Registration Scheduler")
root.geometry("1450x850")
root.configure(bg=BG)
# Track calendar state
current_week_start = datetime.today() - timedelta(days=datetime.today().weekday())
selected = {"day": None, "time": None}
cells = {}
day_labels = []
week_dates = []
# Create reusable label
def make_label(parent, text, size=10, bg=WHITE, fg="black"):
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=("Helvetica", size, "bold"))

# Create reusable entry
def make_entry(parent):
    box = tk.Entry(parent, font=("Helvetica", 10))
    box.pack(fill="x", pady=(2, 8))
    return box


# Create reusable dropdown
def make_dropdown(parent, values):
    box = ttk.Combobox(parent, values=values, state="readonly", font=("Helvetica", 10))
    box.set(values[0])
    box.pack(fill="x", pady=(2, 8))
    return box


# Create reusable button
def make_button(parent, text, command, color):
    tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=("Helvetica", 11, "bold"),
        pady=8,
        cursor="hand2"
    ).pack(fill="x", pady=4)


# Format date
def format_date(date):
    return date.strftime("%a %b %d")

# Get current week dates
def get_week_dates():
    return [current_week_start + timedelta(days=i) for i in range(7)]

# Get selected date
def get_selected_date():
    if selected["day"] is None:
        return None
    return format_date(week_dates[selected["day"]])
# Count registrations for one class slot
def count_registered(date, time, course, location):
    return sum(
        1 for appt in scheduler.get_appointments()
        if appt.date == date
        and appt.time == time
        and appt.course_type == course
        and appt.location == location
    )
# Refresh calendar
def update_calendar():
    global week_dates
    week_dates = get_week_dates()
    course = course_box.get()
    location = location_box.get()
    address_box.config(text="Address:\n" + LOCATIONS[location])
    if selected["day"] is None:
        selected_box.config(text="Selected Class:\nNone selected")
    else:
        selected_box.config(
            text=f"Selected Class:\n{course} | {get_selected_date()} | {selected['time']}"
        )
    for i, date in enumerate(week_dates):
        day_labels[i].config(text=format_date(date))
    for day_index, date in enumerate(week_dates):
        for time in TIMES:
            date_text = format_date(date)
            taken = count_registered(date_text, time, course, location)
            cell = cells[(day_index, time)]

            if taken >= MAX_SEATS:
                cell.config(text="FULL", bg=DARK, fg="white")
            else:
                cell.config(text="Available", bg=COURSE_COLORS[course], fg="black")

    if selected["day"] is not None:
        cells[(selected["day"], selected["time"])].config(bg=SELECTED, fg="black")
# Select calendar time
def select_time(day, time):
    selected["day"] = day
    selected["time"] = time
    update_calendar()
# Move calendar week
def change_week(days):
    global current_week_start
    current_week_start += timedelta(days=days)
    selected["day"] = None
    selected["time"] = None
    update_calendar()
# Search calendar by date
def search_date():
    global current_week_start
    user_input = search_entry.get().strip()
    try:
        searched = datetime.strptime(user_input, "%m/%d/%Y")
    except ValueError:
        try:
            searched = datetime.strptime(user_input, "%m/%d/%y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter a date like 05/12/2026.")
            return
    current_week_start = searched - timedelta(days=searched.weekday())
    selected["day"] = None
    selected["time"] = None
    update_calendar()
# Register student
def register_student():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    if not name or not email or not phone:
        messagebox.showwarning("Missing Information", "Please enter name, email, and phone.")
        return
    if selected["day"] is None:
        messagebox.showwarning("No Time Selected", "Please select a class time.")
        return
    course = course_box.get()
    location = location_box.get()
    date = get_selected_date()
    time = selected["time"]
    new_appointment = Appointment(name, course, location, date, time)
    if scheduler.add_appointment(new_appointment, MAX_SEATS):
        scheduler.save_to_file()
        messagebox.showinfo(
            "Registration Confirmed",
            f"Registration confirmed!\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Course: {course}\n"
            f"Date: {date}\n"
            f"Time: {time}\n"
            f"Location: {location}"
        )
        clear_form()
    else:
        messagebox.showerror("Class Full", "This class is already full.")
# Cancel registration
def cancel_registration():
    if selected["day"] is None:
        messagebox.showwarning("No Time Selected", "Select a class time first.")
        return
    course = course_box.get()
    location = location_box.get()
    date = get_selected_date()
    time = selected["time"]
    for appt in scheduler.get_appointments():
        same_class = (
            appt.course_type == course
            and appt.location == location
            and appt.date == date
            and appt.time == time
        )
        if same_class:
            confirm = messagebox.askyesno(
                "Cancel Registration",
                "Cancel one registration for this class?"
            )
            if confirm:
                scheduler.remove_appointment(appt)
                scheduler.save_to_file()
                update_calendar()
            return
    messagebox.showinfo("No Registration Found", "No registration was found for this selected class.")
# Clear form
def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    selected["day"] = None
    selected["time"] = None
    update_calendar()
# Header
tk.Label(
    root,
    text="Student Class Registration Scheduler",
    bg=DARK,
    fg="white",
    font=("Helvetica", 18, "bold"),
    pady=12
).pack(fill="x")
# Main layout
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=12, pady=12)
left_frame = tk.Frame(main_frame, bg=WHITE, padx=14, pady=14)
left_frame.pack(side="left", fill="y")
right_frame = tk.Frame(main_frame, bg=WHITE, padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True, padx=(12, 0))

# Left form
make_label(left_frame, "Register for a Class", 16, WHITE, DARK).pack(anchor="w", pady=(0, 10))

make_label(left_frame, "Student Name").pack(anchor="w")
name_entry = make_entry(left_frame)

make_label(left_frame, "Email").pack(anchor="w")
email_entry = make_entry(left_frame)

make_label(left_frame, "Phone").pack(anchor="w")
phone_entry = make_entry(left_frame)

make_label(left_frame, "Course").pack(anchor="w")
course_box = make_dropdown(left_frame, COURSES)

make_label(left_frame, "Location").pack(anchor="w")
location_box = make_dropdown(left_frame, list(LOCATIONS.keys()))

address_box = tk.Label(
    left_frame,
    text="",
    bg=OPEN,
    fg="black",
    font=("Helvetica", 9),
    wraplength=260,
    justify="left",
    padx=8,
    pady=8,
    relief="ridge"
)
address_box.pack(fill="x", pady=(0, 10))

selected_box = tk.Label(
    left_frame,
    text="Selected Class:\nNone selected",
    bg="#fee2e2",
    fg="black",
    font=("Helvetica", 9, "bold"),
    wraplength=260,
    justify="left",
    padx=8,
    pady=8,
    relief="ridge"
)
selected_box.pack(fill="x", pady=(0, 10))

make_label(left_frame, "Search Date").pack(anchor="w")
search_entry = make_entry(left_frame)

make_button(left_frame, "Register", register_student, RED)
make_button(left_frame, "Cancel Registration", cancel_registration, DARK)
make_button(left_frame, "Search Date", search_date, "#ef4444")
make_button(left_frame, "Clear Form", clear_form, "#450a0a")

# Calendar navigation
nav_frame = tk.Frame(right_frame, bg=WHITE)
nav_frame.pack(fill="x", pady=(0, 8))
tk.Button(
    nav_frame,
    text="← Previous Week",
    command=lambda: change_week(-7),
    font=("Helvetica", 10, "bold")
).pack(side="left")
tk.Button(
    nav_frame,
    text="Next Week →",
    command=lambda: change_week(7),
    font=("Helvetica", 10, "bold")
).pack(side="right")
make_label(nav_frame, "Click a time slot to select it", 11, WHITE, DARK).pack()

# Calendar grid
grid_frame = tk.Frame(right_frame, bg=WHITE)
grid_frame.pack(fill="both", expand=True)
tk.Label(
    grid_frame,
    text="TIME",
    bg=OPEN,
    fg="black",
    font=("Helvetica", 12, "bold"),
    width=12,
    height=3,
    relief="ridge"
).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
for column in range(7):
    day_label = tk.Label(
        grid_frame,
        text="",
        bg="#fecaca",
        fg="black",
        font=("Helvetica", 12, "bold"),
        width=18,
        height=3,
        relief="ridge"
    )

    day_label.grid(row=0, column=column + 1, padx=2, pady=2, sticky="nsew")
    day_labels.append(day_label)
for row, time in enumerate(TIMES):
    tk.Label(
        grid_frame,
        text=time,
        bg="#fee2e2",
        fg="black",
        font=("Helvetica", 12, "bold"),
        width=12,
        height=3,
        relief="ridge"
    ).grid(row=row + 1, column=0, padx=2, pady=2, sticky="nsew")
    for column in range(7):
        cell = tk.Label(
            grid_frame,
            text="",
            bg=OPEN,
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=18,
            height=4,
            relief="ridge",
            cursor="hand2",
            justify="center"
        )
        cell.grid(row=row + 1, column=column + 1, padx=2, pady=2, sticky="nsew")
        cell.bind(
            "<Button-1>",
            lambda event, day=column, selected_time=time: select_time(day, selected_time)
        )
        cells[(column, time)] = cell
# Grid costumization
for column in range(8):
    grid_frame.columnconfigure(column, weight=1)

for row in range(len(TIMES) + 1):
    grid_frame.rowconfigure(row, weight=1)

# Update when dropdown changes
course_box.bind("<<ComboboxSelected>>", lambda event: update_calendar())
location_box.bind("<<ComboboxSelected>>", lambda event: update_calendar())

# Start program
update_calendar()
root.mainloop()