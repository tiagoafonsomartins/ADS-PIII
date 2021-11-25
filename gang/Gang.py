class Gang:

    def __init__(self, name, course, lesson):
        self.name = name
        self.course = course
        self.lessons = [lesson]

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def __str__(self):
        return "(" + self.name + ")"

    def __repr__(self):
        return str(self)
