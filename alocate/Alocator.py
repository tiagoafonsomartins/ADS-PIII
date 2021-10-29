class Alocator:
    def __init__(self):
        self.classrooms = []
        self.lessons = []

    def add_classrrom(self, classroom):
        self.classrooms.append(classroom)

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def add_classroom_to_lesson(self, lesson, classroom):
        lesson.add_classroom(classroom)
        classroom.add_lesson(lesson)

    #remove

    #removeall

    pass