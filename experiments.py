import time


import csv

from file_manager.Manipulate_Documents import Manipulate_Documents
from alocate.Allocator import Allocator

class Experiments:
    def __init__(self):
        pass

    def test1(self):
        my_list = [1,2,3,4,5]
        print(my_list[-1:])
        print(my_list[:-2])
        print("s" == 's')
        print(range(5))

    def test2(self):
        file = open('Input_Classrooms/Salas.csv')
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
        lessons = md.import_schedule_documents()
        classrooms = md.import_classrooms()
        #print(lessons)
        #print(classrooms)

        a = Allocator()
        for lesson in lessons:
            a.add_lesson(lesson)
        for classroom in classrooms:
            a.add_classroom(classroom)

        simple_schedule = a.simple_allocation()

        md.export_schedule(simple_schedule, "outputMens")


    def test6(self):
        pass

e = Experiments()
e.test5()

