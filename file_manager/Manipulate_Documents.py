import csv
import os

from classroom.Classroom import Classroom
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
                        print(row)
                    f.close()

        return classroom_list

    def export_schedule(self, schedule: list, file_name: str) -> None:
        """
        Export to a csv file the list of Lesson objects

        :param schedule:
        :param file_name:
        :return:
        """
        with open(os.path.join(self.output_path, file_name) + ".csv", 'w', newline='') as file:
            # create the csv writer
            writer = csv.writer(file)

            # write first row with headers
            header = ["Curso", "Unidade de execução", "Turno", "Turma", "Inscritos no turno", "Dia da Semana", "Início", "Fim", "Dia", "Características da sala pedida para a aula",
                      "Sala de aula", "Lotação", "Características reais da sala"]
            writer.writerow(header)

            # write rows to the csv file
            for lesson in schedule:
                writer.writerow(lesson.get_row())


md = Manipulate_Documents()
# md.import_classrooms()
md.export_schedule(md.import_schedule_documents(), "output")

'''def row_to_classroom(self, row: list, nomes_caract: list) -> Classroom:
    """Converts a row from csv file as a list into a Classroom object"""
    caracteristicas = row[5:]
    caract_to_add = []
    for i in len(caracteristicas):
        if caracteristicas[i] == 'X':
            caract_to_add.append(nomes_caract[i])

    return Classroom(row[0], row[1], int(row[2]), int(row[3]), caract_to_add)'''
