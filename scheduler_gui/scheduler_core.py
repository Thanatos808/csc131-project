# Import JSON for saving and loading registration data
import json

# Import Appointment class
from appointment import Appointment


# Scheduler class manages all class registrations
class Scheduler:

    # Create empty appointment list
    def __init__(self):
        self.appointments = []

    # Add a new appointment if the class is not full
    def add_appointment(self, appointment, max_seats=10):
        count = 0

        # Count how many students are already registered for the same class
        for appt in self.appointments:
            same_class = (
                appt.course_type == appointment.course_type and
                appt.location == appointment.location and
                appt.date == appointment.date and
                appt.time == appointment.time
            )

            if same_class:
                count += 1

        # Stop registration if class reached the seat limit
        if count >= max_seats:
            return False

        # Add appointment to the list
        self.appointments.append(appointment)
        return True

    # Return all saved appointments
    def get_appointments(self):
        return self.appointments

    # Remove one appointment
    def remove_appointment(self, appointment):
        if appointment in self.appointments:
            self.appointments.remove(appointment)
            return True

        return False

    # Save appointments to a JSON file
    def save_to_file(self, filename="appointments.json"):
        data = []

        # Convert appointment objects into dictionary format
        for appt in self.appointments:
            data.append({
                "student_name": appt.student_name,
                "course_type": appt.course_type,
                "location": appt.location,
                "date": appt.date,
                "time": appt.time
            })

        # Write registration data into the JSON file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    # Load appointments from a JSON file
    def load_from_file(self, filename="appointments.json"):
        try:
            # Open and read saved registration data
            with open(filename, "r") as file:
                data = json.load(file)

            # Clear current appointment list
            self.appointments = []

            # Convert dictionary data back into Appointment objects
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

        # If no file exists yet, start with an empty list
        except FileNotFoundError:
            self.appointments = []