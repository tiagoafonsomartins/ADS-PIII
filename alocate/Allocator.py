import time

from jmetal.core.solution import PermutationSolution

from classroom import Classroom
from jmetalpy.JMP import JMP
from lesson import Lesson
import numpy as np
import datetime as dt
from metrics.Metric import RoomlessLessons, Overbooking, Underbooking, BadClassroom
from swrlAPI.SWRL_API import query_result


class Allocator:

    def __init__(self, classrooms, schedule, gangs, metrics):  # starting_date, ending_date
        self.classrooms = classrooms
        self.schedule = schedule
        self.gangs = gangs
        self.metrics = metrics
        self.sum_classroom_characteristics = {}

    def sorted_lessons(self) -> list:
        '''
        Sort lessons by day, start time and number of enrolled students

        :return list[Lesson]:
        '''
        return sorted(self.schedule, key=lambda x: (
            x[0].number_of_enrolled_students, time.strptime(x[0].day, '%m/%d/%Y'),
            time.strptime(x[0].start, '%H:%M:%S')))

    def sorted_classrooms(self) -> list:
        '''
        Sort classrooms by normal capacity

        :return list[Classroom]:
        '''
        return sorted(self.classrooms, key=lambda x: (x.normal_capacity, x.rarity, len(x.get_characteristics())))

    def simple_allocation(self) -> list:
        '''
        Simple allocation algorithm that allocates first room that accommodates the lessons requested characteristics
        and is available at that time

        :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
        '''
        lessons_list = self.sorted_lessons()
        classrooms_list = self.sorted_classrooms()

        number_of_roomless_lessons = 0

        schedule = []

        for lesson, c in lessons_list:
            if not c:
                classroom_assigned = False
                for classroom in classrooms_list:
                    if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                            (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()) and \
                            (classroom.is_available(lesson.generate_time_blocks())):
                        classroom.set_unavailable(lesson.generate_time_blocks())
                        schedule.append((lesson, classroom))
                        classroom_assigned = True
                        break

                if not classroom_assigned:
                    if lesson.requested_characteristics != "Não necessita de sala" and \
                            lesson.requested_characteristics != "Lab ISTA":
                        schedule.append((lesson, None))
                        number_of_roomless_lessons += 1
                else:
                    classroom_assigned = False
            else:
                schedule.append((lesson, c))

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

        return schedule

    def allocation_with_overbooking(self, overbooking_percentage: int) -> dict:
        """
        This Algorithm iterates by the schedule and classroom and tries to allocate lessons to classroom if
        every requirement gets fulfilled by the conditions. Then uses JMetalPy to improve some problematic zones of
        our schedule.

        :param overbooking_percentage: percentage of overbooking inputed by the user
        :return:
        """
        lessons_list = self.sorted_lessons()
        classrooms_list = self.sorted_classrooms()
        lessons30 = {}
        number_of_roomless_lessons = 0
        for lesson, c in lessons_list:
            if not c:
                classroom_assigned = False
                for classroom in classrooms_list:
                    if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                            (0 < lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity() *
                             (1 + (overbooking_percentage / 100))) and \
                            (classroom.is_available(lesson.generate_time_blocks())):
                        classroom.set_unavailable(lesson.generate_time_blocks())
                        self.assign_lessons30(lessons30, lesson, classroom)
                        classroom_assigned = True
                        break
                if not classroom_assigned:
                    if lesson.requested_characteristics != "Não necessita de sala" and \
                            lesson.requested_characteristics != "Lab ISTA" and lesson.number_of_enrolled_students != 0:
                        self.assign_lessons30(lessons30, lesson, None)
                        number_of_roomless_lessons += 1
                        # Arq 9/5 com o horário cheio
                        # Laboratórios de informática com demasiados alunos (sala com mais capacidade tem 50, turmas com inscritos que chegam aos 106)
                        # não estou a adicionar lessons que tenham as caracteristicas do if acima
            else:
                self.assign_lessons30(lessons30, lesson, c)

        queryresult = query_result(len(self.metrics))
        troublesome_lessons30_key_list = sorted(lessons30, key=lambda k: len(lessons30[k]))[:5]

        for tbl in troublesome_lessons30_key_list:
            old_metrics = []

            for m in self.metrics:
                m.calculate(lessons30[tbl])
                old_metrics.append(m.get_percentage())

            trouble_l = []
            trouble_c = set()
            for t_l, t_c in lessons30[tbl]:
                trouble_l.append(t_l)
                if t_c is not None:
                    t_c.set_available(t_l.generate_time_blocks())
                    trouble_c.add(t_c)

            if len(trouble_l) > 3:
                new_schedule, jmp_metric_results = JMP().run_algorithm(queryresult, trouble_l, list(trouble_c),
                                                                       self.metrics)
                print("Old metrics", old_metrics, "New metrics", jmp_metric_results)
                if self.new_schedule_is_better(old_metrics, jmp_metric_results, self.metrics,
                                               max(len(trouble_l), len(list(trouble_c)))):
                    lessons30[tbl] = new_schedule

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")
        return lessons30

    def get_classroom_score(self, lesson: Lesson, classroom: Classroom, characs: float, len_characs: float,
                            len_characs_div: float, rarity: float, overbooking: float, underbooking: float):

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

    def weekly_allocation(self, characs=100, len_characs=20, len_characs_div=4, rarity=10, overbooking=50,
                          underbooking=50, use_JMP=True) -> dict:

        '''
                More advanced allocation algorithm that allocates the apparent best fitting room for the presented lesson
                and the same lessons in different weeks

                :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
                '''

        # self.classrooms.sort(key=lambda x: x.normal_capacity)
        self.schedule.sort(key=lambda x: (x[0].gang, x[0].subject, x[0].week_day, time.strptime(x[0].day, '%m/%d/%Y')))
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
                        lesson.course + lesson.subject + lesson.shift + lesson.gang + lesson.week_day) or (
                        cur_classroom and not cur_classroom.is_available(lesson.time_blocks)):
                    last_lesson = (lesson.course + lesson.subject + lesson.shift + lesson.gang + lesson.week_day)
                    cur_score = 0
                    for classroom in self.classrooms:
                        if not classroom.is_available(lesson.time_blocks):
                            continue

                        new_score = self.get_classroom_score(lesson, classroom, characs, len_characs, len_characs_div,
                                                             rarity, overbooking, underbooking)

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

        # print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

        count = 0
        if use_JMP:
            for block, half_hour in lessons30.items():
                room_metric = RoomlessLessons()
                room_metric.calculate(half_hour)

                overbooking_metric = Overbooking()
                overbooking_metric.calculate(half_hour)

                underbooking_metric = Underbooking()
                underbooking_metric.calculate(half_hour)

                bad_classroom_metric = BadClassroom()
                bad_classroom_metric.calculate(half_hour)

                if room_metric.get_percentage() > 0.2 or overbooking_metric.get_percentage() > 0.4 or bad_classroom_metric.get_percentage() > 0.15:
                    # classrooms = []
                    # for classroom in self.classrooms:
                    #    if classroom.is_available([block]):
                    #        classrooms.append(classroom)
                    classrooms = [c for c in self.classrooms if c.is_available([block])]
                    lessons = [item[0] for item in half_hour]

                    if len(lessons) >= 3:
                        count += 1
                        metrics = [RoomlessLessons(), Overbooking(), Underbooking(), BadClassroom()]
                        new_schedule, JMP_metric_results = JMP().run_algorithm(["nsgaii"], lessons, classrooms, metrics)

                        old_metric_results = [room_metric.get_percentage(), overbooking_metric.get_percentage(),
                                              underbooking_metric.get_percentage(),
                                              bad_classroom_metric.get_percentage()]

                        if self.new_schedule_is_better(old_metric_results, JMP_metric_results, metrics,
                                                       max(len(lessons), len(classrooms))):
                            lessons30[block] = new_schedule

        print("Count = ", count)
        return lessons30

    def new_schedule_is_better(self, old_metric_results: list, JMP_metric_results: list, metrics, len_variables):
        new_solution = PermutationSolution(len_variables, len(metrics))
        new_solution.objectives = JMP_metric_results
        old_solution = PermutationSolution(len_variables, len(metrics))
        old_solution.objectives = old_metric_results

        front = [new_solution, old_solution]
        return JMP().get_best_result(front, metrics) == new_solution

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
