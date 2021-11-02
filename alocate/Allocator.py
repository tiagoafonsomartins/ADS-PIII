class Allocator:
    def __init__(self):
        self.classrooms = []
        self.lessons = []
        self.sum_classroom_characteristics = {}

    def add_classroom(self, classroom):
        self.classrooms.append(classroom)
        for characteristic in classroom.get_characteristics():
            print(characteristic)
            if characteristic in self.sum_classroom_characteristics:
                number_of_characteristic = self.sum_classroom_characteristics[characteristic]
            else:
                number_of_characteristic = 0

            self.sum_classroom_characteristics.update({characteristic: number_of_characteristic + 1})

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def sort_lessons(self):
        # sort by day, time, requested characteristics and number of students
        return sorted(self.lessons, key=lambda x: (x.day, x.start, x.number_of_enrolled_students))


    def sort_classrooms(self):
        # sort by type of classroom then by capacity
        return sorted(self.classrooms, key=lambda x: x.normal_capacity)

    def simple_allocation(self):
        sorted_lessons = self.sort_lessons()
        sorted_classrooms = self.sort_classrooms()

        number_of_roomless_lessons = 0

        schedule = []

        for lesson in sorted_lessons:
            for classroom in sorted_classrooms:
                if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                        (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()) and \
                        (classroom.is_available(lesson.generate_time_blocks())):
                    self.add_classroom_to_lesson(lesson, classroom)
                    schedule.append((lesson, classroom))

            if lesson.get_classroom() is None:
                schedule.append((lesson, None))
                number_of_roomless_lessons += 1

        print("There are ", number_of_roomless_lessons, " lessons without a classroom.")
        return schedule


    def get_schedule(self):
        return self.lessons

    def add_classroom_to_lesson(self, lesson, classroom):
        lesson.add_classroom(classroom)
        classroom.set_unavailable(lesson.generate_time_blocks())

    def remove_classroom_from_lesson(self, lesson, classroom):
        lesson.remove_classroom()
        classroom.remove_lesson(lesson)

    def remove_all_allocations(self):
        for lesson in self.lessons:
            lesson.remove_classroom()
        for classroom in self.classrooms:
            classroom.empty_schedule()
