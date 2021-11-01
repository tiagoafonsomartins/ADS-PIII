import csv
import os
from classroom import Classroom

from Classroom import Classroom
from lesson.Lesson import Lesson


class Manipulate_Documents:

    def __init__(self, input_path="../Input_Documents", output_path="../Output_Documents",
                 input_classrooms="../Input_Classrooms"):
        """Basic init for Manipulate_Documents"""
        self.ext = [".csv", ".xml", ".json", ".bd"]
        self.input_path = input_path
        self.output_path = output_path
        self.input_classrooms = input_classrooms

    def import_schedule_documents(self):
        lesson_list = []
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_path, file)
                    f = open(file_to_open, 'r', encoding="utf8")
                    csvreader = csv.reader(f)
                    next(csvreader)
                    for row in csvreader:
                        lesson = Lesson(row[0], row[1], row[2], row[3],
                                        int(row[4]), row[5], row[6], row[7], row[8], row[9])
                        lesson_list.append(lesson)
                    f.close()
        return lesson_list

    def import_classrooms(self):
        classroom_list = []
        for root, dirs, files in os.walk(self.input_classrooms):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_classrooms, file)
                    f = open(file_to_open, 'r', encoding="utf8")
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for row in csvreader:
                        charact_list = []
                        for i in range(5, len(row)):
                            if row[i].lower() == "x":
                                charact_list.append(header[i])
                        classroom = Classroom(row[0], row[1], int(row[2]), int(row[3]), charact_list)
                        classroom_list.append(classroom)
                    f.close()
        return classroom_list


md = Manipulate_Documents()
md.import_schedule_documents()

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
