import sys
import time

import csv

from gang.Gang import Gang
from metrics import Metric
from metrics.Metric import Gaps, UsedRooms, RoomlessLessons, Overbooking, Underbooking
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
        classrooms, rarity_dict = md.import_classrooms()
        gangs, schedule = md.import_schedule_documents(False)

        # print(rarity_dict)
        # print(lessons)
        # print(classrooms)

        c_copy = classrooms.copy()
        g_copy = gangs.copy()
        s_copy = schedule.copy()
        a_simple = Allocator(c_copy, s_copy, g_copy, rarity_dict)

        simple_schedule = a_simple.simple_allocation()
        a_simple.remove_all_allocations()
        start = time.time()
        allocation_with_overbooking = a_simple.allocation_with_overbooking(10)

        room_metric = RoomlessLessons()
        room_metric.calculate(allocation_with_overbooking)

        overbooking_metric = Overbooking()
        overbooking_metric.calculate(allocation_with_overbooking)

        underbooking_metric = Underbooking()
        underbooking_metric.calculate(allocation_with_overbooking)

        print("Roomless Lessons Percentage:", round(room_metric.get_percentage(), 2) * 100, "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_total_metric_value(), 2) * 100, "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_total_metric_value(), 2) * 100, "%")


        elapsed_time = time.time() - start
        print("Elapsed time: ", elapsed_time)

        """all_true = True
        for i in range(len(schedule)):
            if schedule[i][1]:
                print(schedule[i][1]==simple_schedule[i][1])
                if schedule[i][1] != simple_schedule[i][1]:
                    all_true = False
                #print(simple_schedule[i][1])
        print("all_true: ", all_true)"""

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
        dix = {}
        for i in range(10000000):
            dix[str(i)] = i

        start = time.time()
        if '99999999' in dix.keys():
            print("caralho")
        else:
            print('what')
        elapsed_time = time.time() - start

        print("Elapsed time: ", elapsed_time)

    class TestYa:
        def __init__(self, i):
            self.i = i
        def __repr__(self):
            return str(self.i)

    def test14(self):
        l = []
        for i in range(1000):
            l.append((self.TestYa(i), self.TestYa(i)))
        for i, ip1 in l:
            ip1.i = ip1.i + 1

        print(l)

    def test15(self):
        cena = None
        if cena and cena + 1 == 2:
            print("hello")
        else:
            print("Não hello")



def get_tuplo():
    return (1, 2)

e = Experiments()
e.test5()


