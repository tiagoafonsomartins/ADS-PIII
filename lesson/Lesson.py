class Lesson:
    def __init__(self, course: str, subject: str, shift: str, gang: str, number_of_enrolled_students: int, week_day: str, start: str, end: str, day: str, requested_characteristics: str):
        self.course = course
        self.subject = subject
        self.shift = shift
        self.gang = gang
        self.number_of_enrolled_students = number_of_enrolled_students
        self.week_day = week_day
        self.start = start
        self.end = end
        self.day = day
        self.requested_characteristics = requested_characteristics
        self.classroom = None



    def add_classroom(self, classroom):
        self.classroom = classroom
