from abc import ABC, abstractmethod

class Metric(ABC):

    m_type = None

    def __init__(self, name):
        self.name = name
        self.value = []

    @abstractmethod
    def calculate(self, input):
        pass

class Roomless_lessons(Metric):

    def __init__(self):
        super().__init__("Roomless_lessons")
        self.m_type = "lessons"
        self.value.append(0)

    def calculate(self, lesson, classroom):
        if classroom == None: self.value[0] += 1

    def get_roomless_lessons(self):
        return self.value[0]

class Overbooking(Metric):

    def __init__(self):
        self.name = "Overbooking"
        self.m_type = "lessons"

    def calculate(self):
        print("I got the smarts, quick mafs")
        '''lista = [1,2,3]
        for lesson in lessons:
            obj = lista[0]()
            obj.evaluate_metric(input)'''

class Gaps(Metric):

    def __init__(self):
        self.name = "Gaps"
        self.m_type = "gangs"

    def calculate(self):
        print("2+2 is 4, minus 1 is 3 quick mafs")

