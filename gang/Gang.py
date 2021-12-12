class Gang:

    def __init__(self, name, course):
        self.name = name
        self.course = course
        self.schedule = {}

    def add_lesson(self, lesson):
        self.schedule[lesson] = None

    def add_classroom(self, lesson, classroom):
        self.schedule[lesson] = classroom

    def __str__(self):
        return "(" + self.name + ")"

    def __repr__(self):
        return str(self)