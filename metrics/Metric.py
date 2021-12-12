from abc import ABC, abstractmethod

from gang import Gang
from classroom import Classroom
from lesson import Lesson
import time


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
        super().__init__("Overbooking")
        self.name = "Overbooking"
        self.m_type = "lessons"

    def calculate(self, lesson: Lesson, classroom: Classroom):
        if classroom:
            if lesson.number_of_enrolled_students > classroom.normal_capacity:
                self.value.append(classroom.normal_capacity/lesson.number_of_enrolled_students)
            else:
                self.value.append(0)

    def get_total_metric_value(self):
        # return sum(self.value)
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
        self.value = 0

    def calculate(self, input: Gang):
        '''
        Calculates number of gaps that exist in the given gang and stores the value as an attribute
        :param input:
        :return:
        '''
        gang_lessons = input.lessons
        gang_lessons.sort(key=lambda x: (time.strptime(x.day, '%m/%d/%Y'), time.strptime(x.start, '%H:%M:%S')))

        first_lesson = gang_lessons[0]
        last_end = first_lesson.end
        last_day = first_lesson.day
        for lesson in gang_lessons[1:]:
            if lesson.start != last_end and lesson.day == last_day:
                self.value += 1
            last_end = lesson.end

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = 0


class Movements(Metric):

    def __init__(self):
        self.name = "Movements"
        self.m_type = "gangs"
        self.value = 0

    def calculate(self, input: list):
        '''
        Calculates number of Movements that exist in the given gang and stores the value as an attribute
        :param input:
        :return:
        '''
        input.sort(key=lambda x: (time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = input[0][0]
        last_classroom = first_lesson.classroom
        last_day = first_lesson.day
        for association in input[1:]:
            if association[1] != last_classroom and association[0].day == last_day:
                self.value += 1
            last_classroom = association[1]

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = 0


class UsedRooms(Metric):

    def __init__(self):
        self.name = "UsedRooms"
        self.m_type = "lessons"
        self.value = []

    def calculate(self, lesson: Lesson, classroom: Classroom):
        '''
        Receives a Lesson and Classroom and if that Classroom hasn't been recorded it stores the Classroom and updates
        the number of Used Rooms
        :param lesson:
        :param classroom:
        :return:
        '''
        if classroom not in self.value:
            self.value.append(classroom)

    def get_total_metric_value(self):
        return len(self.value)
    
    def reset_metric(self):
        self.value = []


