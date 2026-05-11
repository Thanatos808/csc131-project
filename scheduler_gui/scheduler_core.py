# imports json for saving/loading data 
import json
from appointment import Appointment
# import appointment class 
# scheduler class manages all registrations 
class Scheduler:

# creates appoitment list 
    def __init__(self):
        self.appointments = []
# add a new appoinment if class is not full 
    def add_appointment(self, appointment, max_seats=10):
        count = 0

#count students already registered 
        for appt in self.appointments:
            same_class = (
                appt.course_type == appointment.course_type and
                appt.location == appointment.location and
                appt.date == appointment.date and
                appt.time == appointment.time
            )

            if same_class:
                count += 1
     # stop registration if class is full   
        if count >= max_seats:
            return False
# add appitment to list 
        self.appointments.append(appointment)
        return True
# return all appoitments 
    def get_appointments(self):
        return self.appointments
# remove an appoitment 
    def remove_appointment(self, appointment):
        if appointment in self.appointments:
            self.appointments.remove(appointment)
            return True
        return False
# save appoitments to a json file
    def save_to_file(self, filename="appointments.json"):
        data = []
# convert appoitments into disctionary format
        for appt in self.appointments:
            data.append({
                "student_name": appt.student_name,
                "course_type": appt.course_type,
                "location": appt.location,
                "date": appt.date,
                "time": appt.time
            })
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
 
    def load_from_file(self, filename="appointments.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.appointments = []

            for item in data:
                self.appointments.append(
                    Appointment(
                        item["student_name"],
                        item["course_type"],
                        item["location"],
                        item["date"],
                        item["time"]
                    )
                )

        except FileNotFoundError:
            self.appointments = []