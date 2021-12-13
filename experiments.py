import sys
import time

import csv

from gang.Gang import Gang
from metrics import Metric
from metrics.Metric import Gaps, UsedRooms, RoomlessLessons, Overbooking, Underbooking, BadClassroom, RoomMovements, \
    BuildingMovements, ClassroomInconsistency
from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from alocate.Allocator import Allocator
from lesson.Lesson import Lesson
import random


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
        classrooms = md.import_classrooms()
        gangs, schedule = md.import_schedule_documents("Exemplo_de_horario_primeiro_semestre.csv", False)

        # print(rarity_dict)
        # print(lessons)
        # print(classrooms)

        c_copy = classrooms.copy()
        g_copy = gangs.copy()
        s_copy = schedule.copy()
        a_simple = Allocator(c_copy, s_copy, g_copy)

        print("\nsimple_allocation:\n")

        start = time.time()

        simple_schedule = a_simple.simple_allocation()

        elapsed_time = time.time() - start

        room_metric = RoomlessLessons()
        room_metric.calculate(simple_schedule)

        overbooking_metric = Overbooking()
        overbooking_metric.calculate(simple_schedule)

        underbooking_metric = Underbooking()
        underbooking_metric.calculate(simple_schedule)

        bad_classroom_metric = BadClassroom()
        bad_classroom_metric.calculate(simple_schedule)

        gaps_metric = Gaps()
        gaps_metric.calculate(simple_schedule)

        room_movements_metric = RoomMovements()
        room_movements_metric.calculate(simple_schedule)

        building_movements_metric = BuildingMovements()
        building_movements_metric.calculate(simple_schedule)

        used_rooms_metric = UsedRooms()
        used_rooms_metric.calculate(simple_schedule)

        classroom_inconsistency_metric = ClassroomInconsistency()
        classroom_inconsistency_metric.calculate(simple_schedule)

        print("Roomless Lessons Percentage:", round(room_metric.get_percentage() * 100, 2), "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_percentage() * 100, 2), "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_percentage() * 100, 2), "%")
        print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage() * 100, 2), "%")
        print("Gaps Percentage:", round(gaps_metric.get_percentage() * 100, 2), "%")
        print("Room Movement Percentage:", round(room_movements_metric.get_percentage() * 100, 2), "%")
        print("Building movement Percentage:", round(building_movements_metric.get_percentage() * 100, 2), "%")
        print("Used Rooms Percentage:", round(used_rooms_metric.get_percentage() * 100, 2), "%")
        print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2), "%")
        print("Elapsed time: ", elapsed_time, "\n")

        a_simple.remove_all_allocations()

        print("\nallocation_with_overbooking:\n")
        start = time.time()

        allocation_with_overbooking = a_simple.allocation_with_overbooking(30)

        elapsed_time = time.time() - start

        schedule_nuno = []
        for sublist in allocation_with_overbooking.values():
            for item in sublist:
                schedule_nuno.append(item)

        room_metric = RoomlessLessons()
        room_metric.calculate(schedule_nuno)

        overbooking_metric = Overbooking()
        overbooking_metric.calculate(schedule_nuno)

        underbooking_metric = Underbooking()
        underbooking_metric.calculate(schedule_nuno)

        bad_classroom_metric = BadClassroom()
        bad_classroom_metric.calculate(schedule_nuno)

        gaps_metric = Gaps()
        gaps_metric.calculate(schedule_nuno)

        room_movements_metric = RoomMovements()
        room_movements_metric.calculate(schedule_nuno)

        building_movements_metric = BuildingMovements()
        building_movements_metric.calculate(schedule_nuno)

        used_rooms_metric = UsedRooms()
        used_rooms_metric.calculate(schedule_nuno)

        classroom_inconsistency_metric = ClassroomInconsistency()
        classroom_inconsistency_metric.calculate(schedule_nuno)

        print("Roomless Lessons Percentage:", round(room_metric.get_percentage() * 100, 2), "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_percentage() * 100, 2), "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_percentage() * 100, 2), "%")
        print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage() * 100, 2), "%")
        print("Gaps Percentage:", round(gaps_metric.get_percentage() * 100, 2), "%")
        print("Room Movement Percentage:", round(room_movements_metric.get_percentage() * 100, 2), "%")
        print("Building movement Percentage:", round(building_movements_metric.get_percentage() * 100, 2), "%")
        print("Used Rooms Percentage:", round(used_rooms_metric.get_percentage() * 100, 2), "%")
        print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2), "%")
        print("Elapsed time: ", elapsed_time, "\n")


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
        results = md.import_schedule_documents(True)
        lessons = results[1]

        earliest = "23:59:59"
        latest = "00:00:00"
        for lesson in lessons:
            if lesson[0].start == " " or lesson[0].start == "": continue
            if lesson[0].end == " " or lesson[0].end == "": continue
            new_start = lesson[0].start
            new_end = lesson[0].end
            if len(lesson[0].start) < 8: new_start = "0" + new_start
            if len(lesson[0].end) < 8: new_end = "0" + new_end
            # print(lesson.start)
            # print(lesson.end, "\n")
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
        a, b = get_tuplo()
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
        # m = Movements()
        # m.calculate(gang)
        u_r = UsedRooms()
        u_r.calculate(lesson1, classroom1)
        u_r.calculate(lesson2, classroom1)
        u_r.calculate(lesson3, classroom1)

        print(g.value)
        # print(m.value)
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


    def test16(self):
        md = Manipulate_Documents()
        classrooms = md.import_classrooms()
        gangs, schedule = md.import_schedule_documents(False)
        days = set()
        for i, tuple in enumerate(schedule):
            # if tuple[0].start.split(":")[1] != "00" and tuple[0].start.split(":")[1] != "30":
            # print("Here: ", i)
            # print(tuple[0].end)
            if tuple[0].day not in days:
                days.add(tuple[0].day)
                print(tuple[0].day)
        print(len(days))


    def test17(self):
        l = [1, 2, 3]
        print(l[:2])
        print(l[2:])


    def test18(self):
        md = Manipulate_Documents()
        classrooms = md.import_classrooms()
        gangs, schedule, date = md.import_schedule_documents(False)
        print(date)

        max = 0
        min = 20
        for c in classrooms:
            if len(c.get_characteristics()) > max: max = len(c.get_characteristics())
            if len(c.get_characteristics()) > min: min = len(c.get_characteristics())

        print(max)
        print(min)
        # a = Allocator(classrooms, schedule, gangs)
        # a.get_index_of_block()


    def test19(self):
        l = {}
        l["a"] = 1
        l["b"] = 2

        if "c" in l.keys():
            print("hello")
        else:
            print("Adeus")


    def test20(self):
        # andre_allocation
        md = Manipulate_Documents()
        classrooms = md.import_classrooms()
        gangs, schedule = md.import_schedule_documents("Exemplo_de_horario_primeiro_semestre.csv", False)

        a_simple = Allocator(classrooms, schedule, gangs)

        a_simple.remove_all_allocations()

        start = time.time()

        lessons30 = a_simple.andre_alocation()

        elapsed_time = time.time() - start

        tamanho = sys.getsizeof(lessons30)

        start_convert = time.time()
        schedule_andre = []
        for sublist in lessons30.values():
            for item in sublist:
                schedule_andre.append(item)
        elapsed_time_convert = time.time() - start_convert

        start_metricas = time.time()

        room_metric = RoomlessLessons()
        room_metric.calculate(schedule_andre)

        overbooking_metric = Overbooking()
        overbooking_metric.calculate(schedule_andre)

        underbooking_metric = Underbooking()
        underbooking_metric.calculate(schedule_andre)

        bad_classroom_metric = BadClassroom()
        bad_classroom_metric.calculate(schedule_andre)

        elapsed_time_metricas = time.time() - start_metricas

        print("\n\nandre_algorithm:\n")
        print("Roomless Lessons Percentage:", round(room_metric.get_percentage(), 2) * 100, "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_percentage(), 2) * 100, "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_percentage(), 2) * 100, "%")
        print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage(), 2) * 100, "%")

        print("Elapsed time: ", elapsed_time)
        print("Elapsed time on metricas: ", elapsed_time_metricas)
        print("Elapsed time on convert: ", elapsed_time_convert)
        print("Tamanho do lessons30: ", tamanho)

    def test21(self):
        l = {}
        l["a"] = 1
        l["b"] = 2
        l["c"] = 69

        for block, half_hour in l.items():
            l[block] = 3

        print(l)


def get_tuplo():
    return (1, 2)


e = Experiments()
e.test5()



