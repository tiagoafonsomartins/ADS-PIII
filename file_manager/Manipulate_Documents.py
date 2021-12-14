import csv
import os

from typing import List

from gang.Gang import Gang
from classroom.Classroom import Classroom
from lesson.Lesson import Lesson
import datetime as dt
import time
from django.core.files.uploadedfile import TemporaryUploadedFile
import io


class Manipulate_Documents:

    def __init__(self, input_path="input_documents", output_path="output_documents",
                 input_classrooms="input_classrooms"):
        """
        Basic init for Manipulate_Documents

        :param input_path:
        :param output_path:
        :param input_classrooms:
        """
        self.ext = [".csv", ".xml", ".json", ".bd"]
        self.input_path = input_path
        self.output_path = output_path
        self.input_classrooms = input_classrooms

        self.classroom_list = []

    def import_schedule_documents(self, file_name: str, use_classrooms: bool):
       """
       Imports a csv of a schedule into a list of Lesson objects and Gang (class) objects

       :return: a list with a list Classroom objects and a list of Gang objects
       """
       classroom_dict = {}
       for classroom in self.classroom_list:
           classroom_dict[classroom.name] = classroom
       schedule = []
       gang_list = []

       f = open("./input_documents/Exemplo_de_horario_primeiro_semestre.csv", 'r', encoding="utf8") #todo
       #f = open(self.input_path, 'r', encoding="utf8")

       csvreader = csv.reader(f)
       next(csvreader)
       for row in csvreader:
          self.read_schedule_row(row, use_classrooms, classroom_dict, schedule)
       f.close()
       return gang_list, schedule

    #def import_schedule_documents(self, file_name: TemporaryUploadedFile, use_classrooms: bool):
    #   """
    #   Imports a csv of a schedule into a list of Lesson objects and Gang (class) objects
#
    #   :return: a list with a list Classroom objects and a list of Gang objects
    #   """
    #   classroom_dict = {}
    #   for classroom in self.classroom_list:
    #       classroom_dict[classroom.name] = classroom
    #   schedule = []
    #   gang_list = []
    #   create_gang = True
#
    #   csvreader = csv.reader(io.StringIO(file_name.read().decode('utf-8')))
    #   next(csvreader)
    #   for row in csvreader:
    #       if row[5] and row[6] and row[8]:
    #           lesson = Lesson(row[0], row[1], row[2], row[3],
    #                           int(row[4]), row[5], row[6], row[7], row[8], row[9])
#
    #           if not use_classrooms or not row[10] or row[10] not in classroom_dict.keys():
    #               schedule.append((lesson, None))
    #           else:
    #               classroom_dict[row[10]].set_unavailable(lesson.generate_time_blocks())
    #               schedule.append((lesson, classroom_dict[row[10]]))
#
    #           for gang in gang_list:
    #               if gang.name == lesson.gang:  # TODO tratar de várias turmas para a mesma Lesson
    #                   gang.add_lesson(lesson)
    #                   create_gang = False
    #                   break
    #           if create_gang:
    #               gang_list.append(Gang(lesson.gang, lesson.course))
    #               gang_list[-1].add_lesson(lesson)
    #           else:
    #               create_gang = True
    #   file_name.close()
    #   return gang_list, schedule

    def read_schedule_row(self, row, use_classrooms, classroom_dict, schedule):
        '''
        Reads row of shchedule file
        :param row:
        :param use_classrooms:
        :param classroom_dict:
        :param schedule:
        :return:
        '''
        if row[5] and row[6] and row[8]:
            lesson = Lesson(row[0], row[1], row[2], row[3],
                            int(row[4]), row[5], row[6], row[7], row[8], row[9])

            if not use_classrooms or not row[10] or row[10] not in classroom_dict.keys():
                schedule.append((lesson, None))
            else:
                classroom_dict[row[10]].set_unavailable(lesson.generate_time_blocks())
                schedule.append((lesson, classroom_dict[row[10]]))

    def import_classrooms(self):
        """
        Imports a csv into a list of Classroom objects

        :return: list of Classroom objects
        """

        sum_classroom_characteristics = {}
        #for root, dirs, files in os.walk(self.input_classrooms):
        #    for file in files:
        #        if file.endswith(tuple(self.ext)):
        # file_to_open = os.path.join(self.input_classrooms, file)
        f = open("./input_classrooms/Salas.csv", 'r', encoding="utf8")
        csvreader = csv.reader(f)
        header = next(csvreader)
        for row in csvreader:
            self.read_classroom_row(row, header, sum_classroom_characteristics)
                        # charact_list = []
                        # for i in range(5, len(row)):
                        #     if row[i].lower() == "x":
                        #         charact_list.append(header[i])
                        # classroom = Classroom(row[0], row[1], int(row[2]), int(row[3]), charact_list)
                        # self.classroom_list.append(classroom)
                    #
                    # for characteristic in classroom.get_characteristics():
                    #     if characteristic in sum_classroom_characteristics:
                    #         sum_classroom_characteristics[characteristic] += 1
                    #     else:
                    #         sum_classroom_characteristics[characteristic] = 1

        f.close()
        self.set_classroom_rarities(sum_classroom_characteristics)
        # for classroom in self.classroom_list:
        #     characs = []
        #     for charac in classroom.get_characteristics():
        #         characs.append(sum_classroom_characteristics[charac])
        #     rarity = 1 - (min(characs) / sum(sum_classroom_characteristics.values()))
        #     classroom.set_rarity(rarity)
        return self.classroom_list

    def set_classroom_rarities(self, sum_classroom_characteristics):
        for classroom in self.classroom_list:
            characs = []
            for charac in classroom.get_characteristics():
                characs.append(sum_classroom_characteristics[charac])
            rarity = 1 - (min(characs) / sum(sum_classroom_characteristics.values()))
            classroom.set_rarity(rarity)

    def read_classroom_row(self, row, header, sum_classroom_characteristics):
        '''
        Read row of classroom file
        :param row:
        :param header:
        :param sum_classroom_characteristics:
        :return:
        '''
        charact_list = []
        for i in range(5, len(row)):
            if row[i].lower() == "x":
                charact_list.append(header[i])
        classroom = Classroom(row[0], row[1], int(row[2]), int(row[3]), charact_list)
        self.classroom_list.append(classroom)

        for characteristic in classroom.get_characteristics():
            if characteristic in sum_classroom_characteristics:
                sum_classroom_characteristics[characteristic] += 1
            else:
                sum_classroom_characteristics[characteristic] = 1

    def export_schedule(self, schedule: list, file_name: str) -> None:
        """
        Export to a csv file the list of Lesson objects

        :param schedule: it's a list of tuples like this (Lesson, Classroom)
        :param file_name:
        :return:
        """
        try:
            print(1)
            print(os.path.join(self.output_path, file_name) + ".csv")
            with open(os.path.join(self.output_path, file_name) + ".csv", 'w+', newline='') as file:
                print(2)
                # create the csv writer
                writer = csv.writer(file)

                # write first row with headers
                header = ["Curso", "Unidade de execução", "Turno", "Turma", "Inscritos no turno", "Dia da Semana",
                          "Início",
                          "Fim", "Dia", "Características da sala pedida para a aula",
                          "Sala de aula", "Lotação", "Características reais da sala"]
                writer.writerow(header)

                # write rows to the csv file
                for tuple in schedule:
                    row = tuple[0].get_row()
                    if tuple[1] is not None:
                        row.extend([tuple[1].name, tuple[1].normal_capacity,
                                    self.list_to_comma_sep_string(tuple[1].characteristics)])
                    # print("row: ", row)
                    writer.writerow(row)
        except EnvironmentError as e:  # parent of IOError, OSError *and* WindowsError where available
            print("Something went wrong with creating a file to export the results into")
            print(e)

    def export_schedule_lessons30(self, lessons30: dict, file_name: str) -> None:
        """
        Export to a csv file the list of Lesson objects

        :param schedule: it's a list of tuples like this (Lesson, Classroom)
        :param file_name:
        :return:
        """
        try:

            print(os.path.join(self.output_path, file_name) + ".csv")
            with open(os.path.join(self.output_path, file_name) + ".csv", 'w+', newline='') as file:

                # create the csv writer
                writer = csv.writer(file)

                # write first row with headers
                header = ["Curso", "Unidade de execução", "Turno", "Turma", "Inscritos no turno", "Dia da Semana",
                          "Início",
                          "Fim", "Dia", "Características da sala pedida para a aula",
                          "Sala de aula", "Lotação", "Características reais da sala"]
                writer.writerow(header)

                # write rows to the csv file
                flat_list = []
                for sublist in lessons30.values():
                    for item in sublist:
                        flat_list.append(item)

                for tuple in flat_list:
                    row = tuple[0].get_row()
                    if tuple[1] is not None:
                        row.extend([tuple[1].name, tuple[1].normal_capacity,
                                    self.list_to_comma_sep_string(tuple[1].characteristics)])
                    # print("row: ", row)
                    writer.writerow(row)
        except EnvironmentError as e:  # parent of IOError, OSError *and* WindowsError where available
            print("Something went wrong with creating a file to export the results into")
            print(e)

    def list_to_comma_sep_string(self, my_list: list) -> str:
        """
        Takes a list and returns a string with all its values concatenated with a comma and a space
        :param my_list:
        :return:
        """
        string = ""
        for e in my_list:
            string += str(e) + ", "
        string = string[:-2]
        return string
