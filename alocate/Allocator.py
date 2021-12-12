import time

from classroom import Classroom
from lesson import Lesson
'''Carlos'''

class Allocator:
    def __init__(self, classrooms=[], schedule=[], gangs=[], classrooms_rarity_dict={}):
        self.classrooms = classrooms
        self.schedule = schedule
        self.gangs = gangs
        self.sum_classroom_characteristics = {}
        self.classrooms_rarity_dict = classrooms_rarity_dict

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
        self.schedule.sort(key=lambda x: (x[0].number_of_enrolled_students, time.strptime(x[0].day, '%m/%d/%Y'), time.strptime(x[0].start, '%H:%M:%S'), ))
        # self.lessons.sort(key=lambda x: (x.day, x.start, x.number_of_enrolled_students))

    def sort_classrooms(self) -> list:
        '''
        Sort classrooms by normal capacity

        :return list[Classroom]:
        '''
        for classroom in self.classrooms:
            min_rarity = 20
            for charateristic in classroom.get_characteristics():
                if self.classrooms_rarity_dict[charateristic] < 3 and min_rarity > classroom.rarity:
                    classroom.rarity = 5
                    min_rarity = 5
                elif 3 <= self.classrooms_rarity_dict[charateristic] < 15 and min_rarity > classroom.rarity:
                    classroom.rarity = 4
                    min_rarity = 4
                elif 15 <= self.classrooms_rarity_dict[charateristic] < 71 and min_rarity > classroom.rarity:
                    classroom.rarity = 3
                    min_rarity = 3
                else:
                    classroom.rarity = 2
                    min_rarity = 2
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

    def allocation_with_overbooking(self, overbooking_percentage: int) -> list:
        self.sort_lessons()
        self.sort_classrooms()

        number_of_roomless_lessons = 0
        roomless_lessons = []
        schedule = []

        for lesson, c in self.schedule:
            if not c:
                classroom_assigned = False
                for classroom in self.classrooms:
                    # TODO usar tolerância aqui
                    if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                            (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity() *
                             (1 + (overbooking_percentage/100))) and \
                            (classroom.is_available(lesson.generate_time_blocks())):
                        classroom.set_unavailable(lesson.generate_time_blocks())
                        schedule.append((lesson, classroom))
                        classroom_assigned = True
                        break

                if not classroom_assigned:
                    schedule.append((lesson, None))
                    if lesson.requested_characteristics != "Não necessita de sala" and \
                            lesson.requested_characteristics != "Lab ISTA":
                        # Arq 9/5 com o horário cheio
                        # Laboratórios de informática com demasiados alunos (sala com mais capacidade tem 50, turmas com inscritos que chegam aos 106)
                        roomless_lessons.append((lesson, None))
                        number_of_roomless_lessons += 1
                        print(lesson.get_requested_characteristics(), lesson.get_number_of_enrolled_students(), lesson.datetime_to_string(lesson.day, lesson.start, lesson.end))
                else:
                    classroom_assigned = False
            else:
                schedule.append((lesson, c))
        for c in self.classrooms:
            if "Arq 9" in c.get_characteristics():
                print(c.get_normal_capacity(), c.name, c.schedule)
        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")
        return schedule

    def remove_all_allocations(self) -> None:
        '''
        Remove all allocations from lessons and empty all schedules from classrooms

        :return:
        '''
        for classroom in self.classrooms:
            classroom.empty_schedule()

'''End Carlos'''