import sys
import time

import csv

from gang.Gang import Gang
from metrics import Metric
from metrics.Metric import Movements, Gaps, UsedRooms
from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from alocate.Allocator import Allocator
from lesson.Lesson import Lesson
import numpy as np



class Experiments:
    def __init__(self):
        pass

    def test1(self):
        my_list = [1, 2, 3, 4, 5]
        print(my_list[-1:])
        print(my_list[:-2])
        print("s" == 's')
        print(range(5))

    def test2(self):
        file = open('input_classrooms/Salas.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        row = next(csvreader)
        caracteristicas = row[5:]
        print(row)
        print(caracteristicas)

    def test3(self):
        for i in range(10):
            print(i)

    def test4(self):
        my_list = []
        my_set = set()
        for i in range(10000000):
            my_list.append(str(i))
            my_set.add(str(i))

        start = time.time()
        print("9999999" in my_list)
        elapsed_time = time.time() - start
        print("lista: ", elapsed_time)

        start = time.time()
        print("9999999" in my_set)
        elapsed_time = time.time() - start
        print("set: ", elapsed_time)

    def test5(self):
        md = Manipulate_Documents()
        lessons, gangs = md.import_schedule_documents()
        classrooms = md.import_classrooms()
        print(gangs)
        print(len(gangs))
        # print(lessons)
        # print(classrooms)

        a = Allocator(classrooms, lessons, gangs)
        a.lessons = [l for l in a.lessons if l.start]
        '''for lesson in lessons:
            a.add_lesson(lesson)
        for classroom in classrooms:
            a.add_classroom(classroom)'''

        simple_schedule = a.simple_allocation()

        md.export_schedule(simple_schedule, "outputMens")

    def test6(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(sys.getsizeof(lesson.requested_characteristics))
        print(sys.getsizeof(Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "10:00:00", "10:30:00", "4/23/2005",
                        "Good, Not stinky, Very good")))
        print(sys.getsizeof(""))

    def get_earliest(self):
      pass

    def test7(self):
        md = Manipulate_Documents()
        results = md.import_schedule_documents()
        lessons = results[0]

        earliest = "23:59:59"
        latest = "00:00:00"
        for lesson in lessons:
            if lesson.start == " " or lesson.start == "": continue
            if lesson.end == " " or lesson.end == "": continue
            new_start = lesson.start
            new_end = lesson.end
            if len(lesson.start) < 8: new_start = "0" + new_start
            if len(lesson.end) < 8: new_end = "0" + new_end
            #print(lesson.start)
            #print(lesson.end, "\n")
            print(new_start, "<", earliest)
            if new_start < earliest:
                earliest = new_start
                print(True)
            if new_end > latest:
                latest = new_end


        print("earliest: ", earliest)
        print("latest: ", latest)

    def test8(self):
        string1 = "a"
        string2 = "b"
        print(string1 < string2)


    def test9(self):
        a,b = get_tuplo()
        print(a)
        print(b)

    def test10(self):
        ngosta = getattr(Metric, 'OverBooking')
        atr = ngosta("fdsa", 2)
        atr.testing("fkljdsa")
        print(atr.value)
        print(atr.name)

    def test11(self):
        metrics = [Metric.Overbooking(), Metric.Gaps()]

        for metric in [m for m in metrics if m.m_type == "lesson"]:
            metric.calculate()

    def test12(self):
        lesson1 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        lesson2 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "11:00:00", "12:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        lesson3 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "13:00:00", "15:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        classroom1 = Classroom('Edifício 69', 'Auditório 420', 50, 25, ["cenas"])
        classroom2 = Classroom('Edifício 2', 'B203', 150, 125, ["cenas", "mais cenas", "ainda mais cenas"])
        lesson1.add_classroom(classroom1)
        lesson2.add_classroom(classroom2)
        lesson3.add_classroom(classroom2)

        gang = Gang("best", "lei", lesson1)
        gang.add_lesson(lesson2)
        gang.add_lesson(lesson3)

        g = Gaps()
        g.calculate(gang)
        m = Movements()
        m.calculate(gang)
        u_r = UsedRooms()
        u_r.calculate(lesson1, classroom1)
        u_r.calculate(lesson2, classroom1)
        u_r.calculate(lesson3, classroom1)

        print(g.value)
        print(m.value)
        print(u_r.value)

    def test13(self):
        D = 30
        x = np.random.rand(D)
        print(x)
        f1 = x[0]
        g = 1 + 9 * np.sum(x[1:D] / (D-1))
        h = 1 - np.sqrt(f1 / g)
        f2 = g * h

        print([f1, f2])

        print(np.linspace(0, 1, num=20))

    def test14(self):
        f = 25000.00052
        print(f)



def get_tuplo():
    return (1, 2)

e = Experiments()
e.test14()

