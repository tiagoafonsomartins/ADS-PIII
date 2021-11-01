class Lesson:
    def __init__(self, course: str, subject: str, shift: str, gang: str, number_of_enrolled_students: int,
                 week_day: str, start: str, end: str, day: str, requested_characteristics: str):

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

    def get_row(self):
        return [self.course, self.subject, self.shift, self.gang, str(self.number_of_enrolled_students),
                self.week_day, self.start, self.end, self.day, self.requested_characteristics, self.classroom.name,
                self.classroom.normal_capacity, self.list_to_comma_sep_string(self.classroom.characteristics)]

    def list_to_comma_sep_string(self, my_list):
        str = ""
        for e in my_list:
            str += e + ", "
        str = str[:-2]
        return str

    def add_classroom(self, classroom):
        self.classroom = classroom

    def get_requested_characteristics(self):
        return self.requested_characteristics

    def get_number_of_enrolled_students(self):
        return self.number_of_enrolled_students

    def get_classroom(self):
        return self.classroom

    def remove_classroom(self):
        self.classroom = None
