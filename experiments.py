from file_manager import Manipulate_Documents
import csv

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
        pass

    def test5(self):
        pass

    def test6(self):
        pass

e = Experiments()
e.test1()

