from classroom import Classroom
from lesson import Lesson
'''Carlos'''

class Allocator:
    def __init__(self, classrooms = [], lessons = [], gangs = []):
        self.classrooms = classrooms
        self.lessons = lessons
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
        self.lessons.sort(key=lambda x: (x.day, x.start, x.number_of_enrolled_students))

    def sort_classrooms(self) -> list:
        '''
        Sort classrooms by normal capacity

        :return list[Classroom]:
        '''
        self.classrooms.sort(key=lambda x: x.normal_capacity)

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

        for lesson in self.lessons:
            for classroom in self.classrooms:
                if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                        (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()) and \
                        (classroom.is_available(lesson.generate_time_blocks())):
                    self.add_classroom_to_lesson(lesson, classroom)
                    schedule.append((lesson, classroom))
                    break

            if lesson.get_classroom() is None:
                schedule.append((lesson, None))
                number_of_roomless_lessons += 1

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

        return schedule

    def add_classroom_to_lesson(self, lesson: Lesson, classroom: Classroom) -> None:
        '''
        Allocates classroom to lesson and sets classroom schedule time blocks unavailable

        :param lesson:
        :param classroom:
        :return:
        '''
        lesson.add_classroom(classroom)
        classroom.set_unavailable(lesson.generate_time_blocks())

    def remove_classroom_from_lesson(self, lesson: Lesson, classroom: Classroom) -> None:
        '''
        Remove allocation from lesson and sets classroom schedule time blocks available

        :param lesson:
        :param classroom:
        :return:
        '''
        lesson.remove_classroom()
        classroom.set_available(lesson.generate_time_blocks())

    def remove_all_allocations(self) -> None:
        '''
        Remove all allocations from lessons and empty all schedules from classrooms

        :return:
        '''
        for lesson in self.lessons:
            lesson.remove_classroom()
        for classroom in self.classrooms:
            classroom.empty_schedule()

'''End Carlos'''