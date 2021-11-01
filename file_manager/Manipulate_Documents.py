import csv
import os
from classroom import Classroom

from Classroom import Classroom


class Manipulate_Documents:

    def __init__(self, input_path="Input_Documents", output_path="Output_Documents",
                 input_classrooms="Input_Classrooms"):
        """Basic init for Manipulate_Documents"""
        self.ext = [".csv", ".xml", ".json", ".bd"]
        self.input_path = input_path
        self.output_path = output_path
        self.input_classrooms = input_classrooms

    def import_schedule_documents(self):
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_path, file)
                    f = open(file_to_open, 'r')
                    # meter nas classes necessárias
                    f.close()

    def import_classrooms(self):
        classroom_list = []
        for root, dirs, files in os.walk(self.input_classrooms):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_classrooms, file)
                    f = open(file_to_open, 'r')
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    if f.name == 'Input_Classrooms\Características.csv':
                        print(f.name)
                        for row in csvreader:
                            classroom = Classroom(row[0], row[1], row[2], row[3], [])
                            # classroom_characteristics
                            classroom_list.append(row)
                            # print(classroom_list)
                    # meter nas classes necessárias
                    f.close()

    '''def row_to_classroom(self, row: list, nomes_caract: list) -> Classroom:
        """Converts a row from csv file as a list into a Classroom object"""
        caracteristicas = row[5:]
        caract_to_add = []
        for i in len(caracteristicas):
            if caracteristicas[i] == 'X':
                caract_to_add.append(nomes_caract[i])

        return Classroom(row[0], row[1], int(row[2]), int(row[3]), caract_to_add)'''

    '''def classroom_to_row(self, classroom: Classroom) -> list:
        """Converts a Classroom object into a row for a csv file as a list"""
        return []'''


md = Manipulate_Documents()
md.import_classrooms()