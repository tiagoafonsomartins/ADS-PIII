class Classroom:

    def __init__(self, building: str, name: str, normal_capacity: int, exam_capacity: int, characteristics: list):
        """
        Basic init for Classroom

        :param building:
        :param name:
        :param normal_capacity:
        :param exam_capacity:
        :param characteristics:
        """
        self.schedule = set()  # set("24d13:00-13:30", "13:30-14:00", "14:00-14:30")
        self.building = building
        self.name = name
        self.normal_capacity = normal_capacity
        self.exam_capacity = exam_capacity
        self.characteristics = characteristics
        self.rarity = None


    '''
    def add_lesson(self, lesson):
        self.schedule.append(lesson)
    '''

    def get_characteristics(self):
        return self.characteristics

    def get_normal_capacity(self):
        return self.normal_capacity

    def empty_schedule(self):
        """
        Empty the schedule of the classroom
        """
        self.schedule = set()

    def is_available(self, time_blocks: list) -> bool:
        """
        See if the time block is available in the Classroom schedule

        :param time_blocks:
        :return:
        """
        #print(self.schedule)
        #print(time_blocks)
        for block in time_blocks:
            if block in self.schedule:
                #print(False)
                return False
        #print(True)
        return True

    def set_unavailable(self, time_blocks: list) -> None:
        """
        Allocates the time block in the schedule, making that time block unavailable

        :param time_blocks:
        :return:
        """
        if self.is_available(time_blocks):
            for block in time_blocks:
                self.schedule.add(block)

    def set_rarity(self, rarity: float):
        self.rarity = rarity

    def get_rarity(self):
        return self.rarity

    def __str__(self):
        return "(" + self.building + " | " + self.name + " | " + str(self.normal_capacity) + " | " + str(
            self.exam_capacity) + " | " + str(self.get_characteristics()) + ")"

    def __repr__(self):
        return str(self)
