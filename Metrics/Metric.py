from abc import ABC, abstractmethod
from lesson import Lesson
from classroom import Classroom

class Metric(ABC):

    m_type = None

    def __init__(self, name):
        self.name = name
        self.value = []

    @abstractmethod
    def calculate(self, input):
        pass

    @abstractmethod
    def get_total_metric_value(self):
        pass

    @abstractmethod
    def reset_metric(self):
        pass

class Roomless_Lessons(Metric):

    def __init__(self):
        super().__init__("Roomless_lessons")
        self.m_type = "lessons"
        self.value = 0
        self.total = 0

    def calculate(self, lesson, classroom):
        if classroom == None: self.value += 1
        self.total += 1

    def get_total_metric_value(self):
        return self.value

    def get_percentage(self):
        return self.value/self.total

    def reset_metric(self):
        self.value = 0
        self.total = 0

class Overbooking(Metric):

    def __init__(self):
        self.name = "Overbooking"
        self.m_type = "lessons"

    def calculate(self, lesson: Lesson, classroom: Classroom):
        if lesson.number_of_enrolled_students > classroom.normal_capacity:
            self.value.append(classroom.normal_capacity/lesson.number_of_enrolled_students)
        else:
            self.value.append(0)

    def get_total_metric_value(self):
        return sum(self.value)/len(self.value)

    def reset_metric(self):
        self.value = []

class Underbooking(Metric):

    def __init__(self):
        self.name = "Overbooking"
        self.m_type = "lessons"

    def calculate(self, lesson: Lesson, classroom: Classroom):
        if lesson.number_of_enrolled_students < classroom.normal_capacity:
            self.value.append(lesson.number_of_enrolled_students/classroom.normal_capacity)
        else:
            self.value.append(0)

    def get_total_metric_value(self):
        return sum(self.value)/len(self.value)

    def reset_metric(self):
        self.value = []

class Bad_Classroom(Metric):

    def __init__(self):
        self.name = "Bad_classroom"
        self.m_type = "lessons"
        self.value = 0
        self.total = 0

    def calculate(self, lesson: Lesson, classroom: Classroom):
        characteristics = classroom.characteristics
        if lesson.requested_characteristics not in characteristics:
            self.value += 1
        self.total += 1

    def get_total_metric_value(self):
        return self.value

    def get_percentage(self):
        return self.value / self.total

    def reset_metric(self):
        self.value = 0
        self.total = 0


class Gaps(Metric):

    def __init__(self):
        self.name = "Gaps"
        self.m_type = "gangs"

    def calculate(self):
        print("2+2 is 4, minus 1 is 3 quick mafs")

