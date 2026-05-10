# Stores information for one class registration
class Appointment:
    def __init__(self, student_name, course_type, location, date, time):
        self.student_name = student_name
        self.course_type = course_type
        self.location = location
        self.date = date
        self.time = time
# Easy view of a appointment information as text 
    def __str__(self):
        return f"{self.student_name} - {self.course_type} - {self.location} - {self.date} at {self.time}"
# basic list of infotmation for an appointment, can be changed to include more or less information as needed
    def to_dict(self):
        return {
            "student_name": self.student_name,
            "course_type": self.course_type,
            "location": self.location,
            "date": self.date,
            "time": self.time
        }
    # Create appoitment object from dictionary data 
    @staticmethod
    def from_dict(data):
        return Appointment(
            data["student_name"],
            data["course_type"],
            data["location"],
            data["date"],
            data["time"]
        )