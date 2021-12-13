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

    def has_simultaneous_classes(self):
        blocks = {}
        found = False
        for lesson in self.schedule:
            for block in lesson.time_blocks:
                if block in blocks.keys():
                    print("Found: ", lesson)
                    print("There was: ", blocks[block])
                    found = True
                    break
            for block in lesson.time_blocks:
                blocks[block]=lesson
        if found:
            print(self)
        print("done")
        print(True)