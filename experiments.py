import sys
import time

import csv
from metrics import Metric
from metrics.Metric import Gaps, UsedRooms, RoomlessLessons, Overbooking, Underbooking, BadClassroom, RoomMovements, \
    BuildingMovements, ClassroomInconsistency
from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from lesson.Lesson import Lesson
import random


class Experiments:
    def __init__(self):
        pass

    def test5(self):
        md = Manipulate_Documents()
        classrooms = md.import_classrooms()
        schedule = md.import_schedule_documents("Exemplo_de_horario_primeiro_semestre.csv", False)

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
        print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2),
              "%")
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
        print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2),
              "%")
        print("Elapsed time: ", elapsed_time, "\n")

        print("\nandre_allocation:\n")
        start = time.time()

        weekly_allocation = a_simple.weekly_allocation()

        elapsed_time = time.time() - start

        weekly_schedule = []
        for sublist in weekly_allocation.values():
            for item in sublist:
                weekly_schedule.append(item)

        room_metric = RoomlessLessons()
        room_metric.calculate(weekly_schedule)

        overbooking_metric = Overbooking()
        overbooking_metric.calculate(weekly_schedule)

        underbooking_metric = Underbooking()
        underbooking_metric.calculate(weekly_schedule)

        bad_classroom_metric = BadClassroom()
        bad_classroom_metric.calculate(weekly_schedule)

        gaps_metric = Gaps()
        gaps_metric.calculate(weekly_schedule)

        room_movements_metric = RoomMovements()
        room_movements_metric.calculate(weekly_schedule)

        building_movements_metric = BuildingMovements()
        building_movements_metric.calculate(weekly_schedule)

        used_rooms_metric = UsedRooms()
        used_rooms_metric.calculate(weekly_schedule)

        classroom_inconsistency_metric = ClassroomInconsistency()
        classroom_inconsistency_metric.calculate(weekly_schedule)

        print("Roomless Lessons Percentage:", round(room_metric.get_percentage() * 100, 2), "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_percentage() * 100, 2), "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_percentage() * 100, 2), "%")
        print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage() * 100, 2), "%")
        print("Gaps Percentage:", round(gaps_metric.get_percentage() * 100, 2), "%")
        print("Room Movement Percentage:", round(room_movements_metric.get_percentage() * 100, 2), "%")
        print("Building movement Percentage:", round(building_movements_metric.get_percentage() * 100, 2), "%")
        print("Used Rooms Percentage:", round(used_rooms_metric.get_percentage() * 100, 2), "%")
        print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2),
              "%")
        print("Elapsed time: ", elapsed_time, "\n")

    def test20(self):
        # andre_allocation
        md = Manipulate_Documents()
        classrooms = md.import_classrooms()
        gangs, schedule = md.import_schedule_documents("Exemplo_de_horario_primeiro_semestre.csv", False)

        a_simple = Allocator(classrooms, schedule, gangs)

        a_simple.remove_all_allocations()

        start = time.time()

        lessons30 = a_simple.andre_alocation(use_JMP=True)

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

        print(schedule_andre)

        print("\n\nandre_algorithm:\n")
        print("Roomless Lessons Percentage:", round(room_metric.get_percentage(), 2) * 100, "%")
        print("Overbooking Percentage:", round(overbooking_metric.get_percentage(), 2) * 100, "%")
        print("Underbooking Percentage:", round(underbooking_metric.get_percentage(), 2) * 100, "%")
        print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage(), 2) * 100, "%")

        print("Elapsed time: ", elapsed_time)
        print("Elapsed time on metricas: ", elapsed_time_metricas)
        print("Elapsed time on convert: ", elapsed_time_convert)
        print("Tamanho do lessons30: ", tamanho)



def get_tuplo():
    return (1, 2)


e = Experiments()
e.test5()
