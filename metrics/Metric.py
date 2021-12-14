import datetime
from abc import ABC, abstractmethod
from jmetal.core.problem import Problem
from classroom import Classroom
from lesson import Lesson
import time


class Metric(ABC):
    m_type = None

    def __init__(self, name):
        self.name = name
        self.value = []
        self.weight = 0.5

    @abstractmethod
    def calculate(self, input):
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
            if lesson.requested_characteristics != "Não necessita de sala" and not classroom:
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
        self.value = []

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the Over Booking of the lessons
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:
            if classroom and lesson.number_of_enrolled_students > classroom.normal_capacity:
                #self.value.append((lesson.number_of_enrolled_students - classroom.normal_capacity) / classroom.normal_capacity)
                 self.value.append(classroom.normal_capacity / lesson.number_of_enrolled_students)
                # self.value.append(lesson.number_of_enrolled_students - classroom.normal_capacity)
            else:
                self.value.append(0)

    def get_percentage(self):
        return sum(self.value) / len(self.value)

    def reset_metric(self):
        self.value = []


class Underbooking(Metric):

    def __init__(self):
        super().__init__("Underbooking")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"
        self.weight = 0.25

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the UnderBooking of the lessons
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:

            if classroom and lesson.number_of_enrolled_students < classroom.normal_capacity:
                #self.value.append(
                    #(classroom.normal_capacity - lesson.number_of_enrolled_students) / classroom.normal_capacity)
                self.value.append(lesson.number_of_enrolled_students / classroom.normal_capacity)
            else:
                self.value.append(0)

    def get_percentage(self):
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
        self.value = []

    def calculate(self, schedule: list):
        '''
        Calculates number of gaps that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''

        schedule.sort(key=lambda x: (x[0].gang, time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_day_lesson = schedule[0][0]
        previous_lesson = first_day_lesson

        lesson_blocks = 0
        day_gapping = []

        for lesson, classroom in schedule[1:]:

            if previous_lesson.gang != lesson.gang:
                self.value.append((int((sum([e[0] for e in day_gapping]))), int(sum([e[1] for e in day_gapping]))))

                previous_lesson = lesson
                first_day_lesson = lesson
                lesson_blocks = 0
                day_gapping = []
                continue

            if lesson.day != previous_lesson.day:
                day_blocks = self.blocks_in_interval(previous_lesson.end, first_day_lesson.start)
                day_gapping.append((day_blocks - lesson_blocks, day_blocks))

                first_day_lesson = lesson
                previous_lesson = lesson
                lesson_blocks = 0
                continue

            for block in lesson.time_blocks:
                if block not in previous_lesson.time_blocks:
                    lesson_blocks += 1

            previous_lesson = lesson

    def blocks_in_interval(self, time1, time2):
        time1_split = time1.split(":")
        time2_split = time2.split(":")

        t1 = datetime.timedelta(hours=int(time1_split[0]), minutes=int(time1_split[1]))
        t2 = datetime.timedelta(hours=int(time2_split[0]), minutes=int(time2_split[1]))
        t3 = datetime.timedelta(hours=0, minutes=30)

        return (t1 - t2) / t3

    def get_total_metric_value(self):
        return sum([e[0] for e in self.value]) / len(self.value)

    def get_percentage(self):
        return sum([e[0] for e in self.value]) / sum([e[1] for e in self.value])

    def reset_metric(self):
        self.value = []


class RoomMovements(Metric):

    def __init__(self):
        super().__init__("RoomMovements")
        self.objective = Problem.MINIMIZE
        self.m_type = "gangs"
        self.value = []

    def calculate(self, schedule: list):
        '''
        Calculates number of RoomMovements that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''
        schedule.sort(key=lambda x: (x[0].gang, time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = schedule[0][0]
        previous_classroom = schedule[0][1]
        previous_lesson = first_lesson

        movements = 0
        possible_movements = 0
        for lesson, classroom in schedule[1:]:

            if previous_lesson.gang != lesson.gang:
                self.value.append((movements, possible_movements))
                previous_lesson = lesson
                previous_classroom = classroom
                movements = 0
                possible_movements = 0

                continue

            if lesson.day != previous_lesson.day:
                previous_lesson = lesson
                previous_classroom = classroom
                continue

            if classroom != previous_classroom:
                movements += 1

            possible_movements += 1
            previous_classroom = classroom
            previous_lesson = lesson

    def get_total_metric_value(self):
        return sum([m[0] for m in self.value]) / len(self.value)

    def get_percentage(self):
        return sum([m[0] for m in self.value]) / sum([m[1] for m in self.value])

    def reset_metric(self):
        self.value = []


class BuildingMovements(Metric):

    def __init__(self):
        super().__init__("BuildingMovements")
        self.objective = Problem.MINIMIZE
        self.m_type = "gangs"
        self.value = []

    def calculate(self, schedule: list):
        '''
        Calculates number of BuildingMovements that exist in the given gang and stores the value as an attribute
        :param schedule:
        :return:
        '''
        schedule.sort(key=lambda x: (x[0].gang, time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S')))

        first_lesson = schedule[0][0]
        previous_classroom = schedule[0][1]
        previous_lesson = first_lesson

        movements = 0
        possible_movements = 0
        for lesson, classroom in schedule[1:]:

            if previous_lesson.gang != lesson.gang:
                self.value.append((movements, possible_movements))
                previous_lesson = lesson
                previous_classroom = classroom
                movements = 0
                possible_movements = 0
                continue

            if lesson.day != previous_lesson.day:
                previous_lesson = lesson
                previous_classroom = classroom
                continue

            if classroom and previous_classroom and classroom.building != previous_classroom.building:
                movements += 1

            possible_movements += 1
            previous_classroom = classroom
            previous_lesson = lesson

    def get_total_metric_value(self):
        return sum([m[0] for m in self.value]) / len(self.value)

    def get_percentage(self):
        return sum([m[0] for m in self.value]) / sum([m[1] for m in self.value])

    def reset_metric(self):
        self.value = []


class UsedRooms(Metric):

    def __init__(self):
        super().__init__("UsedRooms")
        self.objective = Problem.MINIMIZE
        self.m_type = "lessons"
        self.value = []
        self.total = 0

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the number of Used Rooms
        :param schedule:
        :return:
        '''
        for lesson, classroom in schedule:
            self.total += 1
            if classroom not in self.value:
                self.value.append(classroom)

    def get_total_metric_value(self):
        return len(self.value)

    def get_percentage(self):
        return len(self.value) / self.total

    def reset_metric(self):
        self.value = []
        self.total = 0


class ClassroomInconsistency(Metric):

    def __init__(self):
        super().__init__("ClassroomInconsistency")
        self.objective = Problem.MAXIMIZE
        self.m_type = "gangs"
        self.value = []

    def calculate(self, schedule: list):
        '''
        Receives a Schedule and calculates the ClassroomInconsistency
        :param schedule:
        :return:
        '''
        schedule.sort(key=lambda x: (x[0].gang, x[0].subject, x[0].week_day, time.strptime(x[0].day, '%m/%d/%Y')))

        previous_lesson = schedule[0][0]
        previous_classroom = schedule[0][1]

        inc = 0
        possible_inc = 0
        for lesson, classroom in schedule[1:]:
            if lesson.gang != previous_lesson.gang:
                self.value.append((inc, possible_inc))

                previous_lesson = lesson
                previous_classroom = classroom
                inc = 0
                possible_inc = 0
                continue

            if lesson.subject != previous_lesson.subject or lesson.week_day != previous_lesson.week_day:
                previous_lesson = lesson
                previous_classroom = classroom
                continue

            if previous_classroom != classroom:
                inc += 1

            previous_lesson = lesson
            previous_classroom = classroom
            possible_inc += 1


    def get_total_metric_value(self):
        return sum([m[0] for m in self.value]) / len(self.value)

    def get_percentage(self):
        return sum([m[0] for m in self.value]) / sum([m[1] for m in self.value])

    def reset_metric(self):
        self.value = []
