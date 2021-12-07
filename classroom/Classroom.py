'''Nuno'''

class Classroom:
    def __init__(self, building: str, name: str, normal_capacity: int, exam_capacity: int, characteristics: list):
        self.schedule = set()  # set("24d13:00-13:30", "13:30-14:00", "14:00-14:30")
        self.building = building
        self.name = name
        self.normal_capacity = normal_capacity
        self.exam_capacity = exam_capacity
        self.characteristics = characteristics

    '''
    def add_lesson(self, lesson):
        self.schedule.append(lesson)
    '''

    def get_characteristics(self):
        return self.characteristics

    def get_normal_capacity(self):
        return self.normal_capacity

    def empty_schedule(self):
        self.schedule = set()

    def is_available(self, time_blocks: list) -> bool:
        for block in time_blocks:
            if block in self.schedule:
                return False
        return True

    def set_unavailable(self, time_blocks: list) -> None:
        if self.is_available(time_blocks):
            for block in time_blocks:
                self.schedule.add(block)
    '''End Nuno'''

    def __str__(self):
        return "(" + self.building + " | " + self.name + " | " + str(self.normal_capacity) + " | " + str(self.exam_capacity) + ")"

    def __repr__(self):
        return str(self)