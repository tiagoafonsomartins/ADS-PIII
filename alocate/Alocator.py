class Allocator:
    def __init__(self):
        self.classrooms = []
        self.lessons = []
        self.sum_classroom_characteristics = {}

    def add_classroom(self, classroom):
        self.classrooms.append(classroom)
        for characteristic in classroom.get_characteristics():
            number_of_characteristic = self.sum_classroom_characteristics[characteristic]
            self.sum_classroom_characteristics.update({characteristic: number_of_characteristic + 1})

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def sort_lessons(self):
        # sort by day, time, requested characteristics and number of students
        self.lessons.sort(key=lambda x: (x.day, x.start, x.requested_characteristics, x.number_of_enrolled_students))

    def sort_classrooms(self):
        # sort by type of classroom then by capacity
        self.classrooms.sort(key=lambda x: (x.characteristics, x.normal_capacity))

    def simple_allocation(self):
        number_of_roomless_lessons = 0

        for lesson in self.lessons:
            for classroom in self.classrooms:
                if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                        (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()):
                    self.add_classroom_to_lesson(lesson, classroom)

            if lesson.get_classroom() is None:
                number_of_roomless_lessons += 1

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

    def add_classroom_to_lesson(self, lesson, classroom):
        lesson.add_classroom(classroom)
        classroom.add_lesson(lesson)

    def remove_classroom_from_lesson(self, lesson, classroom):
        lesson.remove_classroom()
        classroom.remove_lesson(lesson)

    def remove_all_allocations(self):
        for lesson in self.lessons:
            lesson.remove_classroom()
        for classroom in self.classrooms:
            classroom.remove_all_lessons()
