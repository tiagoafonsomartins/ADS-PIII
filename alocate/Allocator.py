import time

from classroom import Classroom
from jmetalpy.JMP import JMP
from lesson import Lesson
import numpy as np
import datetime as dt

from metrics.Metric import RoomlessLessons, Overbooking
from swrlAPI.SWRL_API import query_result


class Allocator:

    def __init__(self, classrooms, schedule, gangs):  # starting_date, ending_date
        self.classrooms = classrooms
        self.schedule = schedule
        self.gangs = gangs
        self.sum_classroom_characteristics = {}

    def add_classroom(self, classroom: Classroom) -> None:
        '''
        Add object classroom to list of classrooms and count number of type of characteristics

        :param classroom:
        :return:
        '''
        self.classrooms.append(classroom)
        for characteristic in classroom.get_characteristics():
            if characteristic in self.sum_classroom_characteristics:
                number_of_characteristic = self.sum_classroom_characteristics[characteristic]
            else:
                number_of_characteristic = 0

            self.sum_classroom_characteristics.update({characteristic: number_of_characteristic + 1})

    def add_lesson(self, lesson: Lesson) -> None:
        '''
        Add object lesson to list of lessons

        :param lesson:
        :return:
        '''
        self.lessons.append(lesson)

    def sort_lessons(self) -> list:
        '''
        Sort lessons by day, start time and number of enrolled students

        :return list[Lesson]:
        '''
        self.schedule.sort(key=lambda x: (
            x[0].number_of_enrolled_students, time.strptime(x[0].day, '%m/%d/%Y'),
            time.strptime(x[0].start, '%H:%M:%S'),))
        # self.lessons.sort(key=lambda x: (x.day, x.start, x.number_of_enrolled_students))

    def sort_classrooms(self) -> list:
        '''
        Sort classrooms by normal capacity

        :return list[Classroom]:
        '''
        self.classrooms.sort(key=lambda x: (x.normal_capacity, x.rarity, len(x.get_characteristics())))

    def simple_allocation(self) -> list:
        '''
        Simple allocation algorithm that allocates first room that accommodates the lessons requested characteristics
        and is available at that time

        :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
        '''
        self.sort_lessons()
        self.sort_classrooms()

        number_of_roomless_lessons = 0

        schedule = []

        for lesson, c in self.schedule:
            if not c:
                classroom_assigned = False
                for classroom in self.classrooms:
                    # TODO usar tolerância aqui
                    if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                            (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()) and \
                            (classroom.is_available(lesson.generate_time_blocks())):
                        classroom.set_unavailable(lesson.generate_time_blocks())
                        schedule.append((lesson, classroom))
                        classroom_assigned = True
                        break

                if not classroom_assigned:
                    schedule.append((lesson, None))
                    number_of_roomless_lessons += 1
                else:
                    classroom_assigned = False
            else:
                schedule.append((lesson, c))

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

        return schedule

    def allocation_with_overbooking(self, overbooking_percentage: int) -> dict:
        self.sort_lessons()
        self.sort_classrooms()
        lessons30 = {}
        number_of_roomless_lessons = 0
        for lesson, c in self.schedule:
            if not c:
                classroom_assigned = False
                for classroom in self.classrooms:
                    if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                            (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity() *
                             (1 + (overbooking_percentage / 100))) and \
                            (classroom.is_available(lesson.generate_time_blocks())):
                        classroom.set_unavailable(lesson.generate_time_blocks())
                        self.assign_lessons30(lessons30, lesson, classroom)
                        classroom_assigned = True
                        break
                if not classroom_assigned:
                    if lesson.requested_characteristics != "Não necessita de sala" and \
                            lesson.requested_characteristics != "Lab ISTA":
                        self.assign_lessons30(lessons30, lesson, None)
                        number_of_roomless_lessons += 1
                        # Arq 9/5 com o horário cheio
                        # Laboratórios de informática com demasiados alunos (sala com mais capacidade tem 50, turmas com inscritos que chegam aos 106)
                        # não estou a adicionar lessons que tenham as caracteristicas do if acima
            else:
                self.assign_lessons30(lessons30, lesson, c)

        troublesome_lessons30 = max(lessons30, key=lambda k: len(lessons30[k]))
        rll = RoomlessLessons()
        rll.calculate(lessons30[troublesome_lessons30])
        ob = Overbooking()
        ob.calculate(lessons30[troublesome_lessons30])

        # print("before", rll.get_total_metric_value(), ob.get_total_metric_value())
        trouble_l = []
        trouble_c = set()
        for t_l, t_c in lessons30[troublesome_lessons30]:
            trouble_l.append(t_l)
            trouble_c.add(t_c)
        metrics = [RoomlessLessons(), Overbooking()]
        JMP().run_algorithm(query_result()[0], trouble_l, list(trouble_c), metrics)

        # print(lessons30)
        # print("There are ", number_of_roomless_lessons, " lessons without a classroom.")
        return lessons30

    def get_classroom_score(self, lesson: Lesson, classroom: Classroom, characs: float, len_characs: float,
                            len_characs_div: float, rarity: float, overbooking: float, underbooking: float):
        # if not classroom.is_available(lesson.generate_time_blocks()): return 0

        score = 0

        if lesson.get_requested_characteristics() in classroom.get_characteristics(): score += characs
        score += (len_characs - len(classroom.get_characteristics())) / len_characs_div
        score += (1 - classroom.get_rarity()) * rarity
        if lesson.number_of_enrolled_students > classroom.normal_capacity:
            score += (classroom.normal_capacity / lesson.number_of_enrolled_students) * overbooking
        else:
            score += overbooking
        if lesson.number_of_enrolled_students < classroom.normal_capacity:
            score += (lesson.number_of_enrolled_students / classroom.normal_capacity) * underbooking
        else:
            score += underbooking

        return score

    def andre_alocation(self, characs=100, len_characs=20, len_characs_div=4, rarity=10, overbooking=50,
                        underbooking=50) -> list:
        '''
                More advanced allocation algorithm that allocates the apparent best fitting room for the presented lesson
                and the same lessons in different weeks

                :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
                '''

        # self.classrooms.sort(key=lambda x: x.normal_capacity)
        number_of_roomless_lessons = 0
        lessons30 = {}
        last_lesson = ""
        cur_classroom = None
        cur_score = 0

        for lesson, c in self.schedule:
            if not c:
                if lesson.requested_characteristics == "Não necessita de sala":
                    self.assign_lessons30(lessons30, lesson, None)
                    continue

                if last_lesson != (
                        lesson.course + lesson.subject + lesson.shift + lesson.gang + lesson.week_day) or not cur_classroom.is_available(
                    lesson.time_blocks):
                    last_lesson = (lesson.course + lesson.subject + lesson.shift + lesson.gang + lesson.week_day)
                    cur_score = 0
                    for classroom in self.classrooms:
                        if not classroom.is_available(lesson.time_blocks):
                            continue
                        new_score = self.get_classroom_score(lesson, classroom, )
                        if new_score > cur_score:
                            cur_classroom = classroom
                            cur_score = new_score

                if cur_classroom is None:
                    self.assign_lessons30(lessons30, lesson, None)
                    number_of_roomless_lessons += 1
                    continue

                cur_classroom.set_unavailable(lesson.time_blocks)
                self.assign_lessons30(lessons30, lesson, cur_classroom)

            else:
                cur_classroom.set_unavailable(lesson.time_blocks)
                self.assign_lessons30(lessons30, lesson, c)

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

        return lessons30

    def assign_lessons30(self, lessons30, lesson, classroom):
        if lesson.time_blocks[0] in lessons30.keys():
            lessons30[lesson.time_blocks[0]].append((lesson, classroom))  # schedule.append((lesson, classroom))
        else:
            lessons30[lesson.time_blocks[0]] = [(lesson, classroom)]

    def get_num_of_blocks(self) -> int:
        days = set()
        for i, tuple in enumerate(self.schedule):
            if tuple[0].day not in days:
                days.add(tuple[0].day)
                print(tuple[0].day)
        return len(days)

    def numOfDays(start, end):
        return np.busday_count(start, end)

    def get_block(self, month: str, day: str, year: str, start_time: str, end_time: str):
        return month + "/" + day + "/" + year + "_" + start_time + "-" + end_time

    # "10/16/2015_09:30:00-10:00:00"
    def get_index_of_block(self, block: str) -> int:
        if not isinstance(block, str): return -1
        if "_" not in block or "-" not in block: return -1
        if block.find("_") > block.find("-"): return -1

        index = 0

        date, time = block.split("_")
        month, day, year = date.split("/")
        time = time.split("-")[0]
        hour, minute = time.split(":")[:2]
        date = dt.date(int(year), int(month), int(day))

        if date < self.starting_date: return -1
        if int(hour) < 8: return -1

        days_between = self.numOfDays(self.starting_date, date)

        index += days_between * 32
        index += (int(hour) - 8) * 2
        if minute == "30": index += 1

        return index

    def remove_all_allocations(self) -> None:
        '''
        Remove all allocations from lessons and empty all schedules from classrooms

        :return:
        '''
        for classroom in self.classrooms:
            classroom.empty_schedule()
