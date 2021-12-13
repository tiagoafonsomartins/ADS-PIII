from abc import ABC, abstractmethod
from jmetal.core.problem import Problem
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


class RoomlessLessons(Metric):

    def __init__(self):
        super().__init__("Roomless_lessons")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"
        self.value = 0
        self.total = 0

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the number of lessons without classrooms
        :param schedule:
        :return:
        '''
        # if classroom == None: self.value += 1
        # self.total += 1
        for lesson, classroom in schedule:
            self.total += 1
            if not classroom:
                self.value += 1

    def get_total_metric_value(self):
        return self.value

    def get_percentage(self):
        return self.value / self.total

    def reset_metric(self):
        self.value = 0
        self.total = 0


class Overbooking(Metric):

    def __init__(self):
        super().__init__("Overbooking")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the Over Booking of the lessons
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:
            if classroom:
                if lesson.number_of_enrolled_students > classroom.normal_capacity:
                    self.value.append(classroom.normal_capacity / lesson.number_of_enrolled_students)
                    # self.value.append(lesson.number_of_enrolled_students - classroom.normal_capacity)
                else:
                    self.value.append(0)

    def get_total_metric_value(self):
        # return sum(self.value)
        return sum(self.value) / len(self.value)

    def reset_metric(self):
        self.value = []


class Underbooking(Metric):

    def __init__(self):
        super().__init__("Underbooking")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the UnderBooking of the lessons
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:

            if classroom and lesson.number_of_enrolled_students < classroom.normal_capacity:

                self.value.append(lesson.number_of_enrolled_students / classroom.normal_capacity)
            else:
                self.value.append(0)

    def get_total_metric_value(self):
        return sum(self.value) / len(self.value)

    def reset_metric(self):
        self.value = []


class BadClassroom(Metric):

    def __init__(self):
        super().__init__("Bad_classroom")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"
        self.value = 0
        self.total = 0

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the number of lessons without classroom with requested characteristics
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:
            if classroom and lesson.requested_characteristics not in classroom.characteristics:
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
        super().__init__("Gaps")
        self.objective = Problem.MINIMIZE
        self.m_type = "gangs"
        self.value = 0

    def calculate(self, schedule: dict):
        '''
        Calculates number of gaps that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''

        s = [(k, v) for k, v in schedule.items()]

        s.sort(key=lambda x: (
            time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = s[0][0]
        last_end = first_lesson.end
        last_day = first_lesson.day
        for lesson, classroom in s[1:]:
            if lesson.start != last_end and lesson.day == last_day:
                self.value += 1
            last_end = lesson.end

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = 0


class RoomMovements(Metric):

    def __init__(self):
        super().__init__("RoomMovements")
        self.objective = Problem.MINIMIZE
        self.m_type = "gangs"
        self.value = 0

    def calculate(self, schedule: dict):
        '''
        Calculates number of RoomMovements that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''
        s = [(k, v) for k, v in schedule.items()]

        s.sort(key=lambda x: (
            time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = s[0][0]
        last_classroom = first_lesson.classroom
        last_day = first_lesson.day
        for lesson, classroom in s[1:]:
            if classroom != last_classroom and lesson.day == last_day:
                self.value += 1
            last_classroom = classroom

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = 0


class BuildingMovements(Metric):

    def __init__(self):
        super().__init__("BuildingMovements")
        self.objective = Problem.MINIMIZE
        self.m_type = "gangs"
        self.value = 0

    def calculate(self, schedule: list):
        '''
        Calculates number of BuildingMovements that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''
        s = [(k, v) for k, v in schedule.items()]

        s.sort(key=lambda x: (
            time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = s[0][0]
        previous_classroom = first_lesson.classroom
        previous_day = first_lesson.day
        for lesson, classroom in s[1:]:
            if classroom.building != previous_classroom.building and lesson.day == previous_day:
                self.value += 1
            previous_classroom = classroom
            previous_day = lesson.day

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = 0


class UsedRooms(Metric):

    def __init__(self):
        super().__init__("UsedRooms")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"
        self.value = []

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the number of Used Rooms
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:
            if classroom not in self.value:
                self.value.append(classroom)

    def get_total_metric_value(self):
        return len(self.value)

    def reset_metric(self):
        self.value = []


class ClassroomConsistency(Metric):

    def __init__(self):
        super().__init__("UsedRooms")
        self.objective = Problem.MAXIMIZE
        self.m_type = "gangs"
        self.value = 0

    def calculate(self, schedule: dict):
        '''
        Receives a Schedule and calculates the ClassroomConsistency
        :param schedule:
        :return:
        '''
        s = [(k, v) for k, v in schedule.items()]

        previous_lesson = s[0][0]
        previous_classroom = s[0][1]
        for lesson, classroom in s[1:]:
            if (lesson.course == previous_lesson.course and lesson.subject == previous_lesson.subject and
                lesson.shift == previous_lesson.shift and lesson.week_day == previous_lesson.week_day) and \
                    classroom == previous_classroom:
                self.value += 1

    def get_total_metric_value(self):
        return self.value

    def reset_metric(self):
        self.value = []
