import time

from classroom import Classroom
from lesson import Lesson
'''Carlos'''

class Allocator:
    def __init__(self, classrooms = [], schedule = [], gangs = []):
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
        self.schedule.sort(key=lambda x: (time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S'), x[0].number_of_enrolled_students))
        # self.lessons.sort(key=lambda x: (x.day, x.start, x.number_of_enrolled_students))

    def sort_classrooms(self) -> list:
        '''
        Sort classrooms by normal capacity

        :return list[Classroom]:
        '''
        self.classrooms.sort(key=lambda x: (x.normal_capacity, len(x.get_characteristics())))

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

    def andre_alocation(self) -> list:
        '''
                Simple allocation algorithm that allocates first room that accommodates the lessons requested characteristics
                and is available at that time

                :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
                '''
        self.classrooms.sort(key=lambda x: x.normal_capacity)
        number_of_roomless_lessons = 0
        schedule = []
        cur_class = ""
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

    def get_num_of_blocks(self) -> int:
        days = set()
        for i, tuple in enumerate(self.schedule):
            if tuple[0].day not in days:
                days.add(tuple[0].day)
                print(tuple[0].day)
        return len(days)

    # "10/16/2015_09:30:00-10:00:00"
    def get_index_of_block(self,starting_block: str, block: str) -> int:
        if not isinstance(block, str): return ("", "", "")
        if "_" not in block or "-" not in block: return ("", "", "")
        if block.find("_") > block.find("-"): return ("", "", "")

        date, time = block.split("_")
        s_date, s_time = starting_block.split("_")
        month, day, year = date.split("/")
        s_month, s_day, s_year = s_date.split("/")
        start = time.split("-")[0]
        hour, minute = start.split(":")[:2]

        index = 0

        index +=
    def remove_all_allocations(self) -> None:
        '''
        Remove all allocations from lessons and empty all schedules from classrooms

        :return:
        '''
        for classroom in self.classrooms:
            classroom.empty_schedule()
