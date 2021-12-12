import csv
import os

from typing import List

from gang.Gang import Gang
from classroom.Classroom import Classroom
from lesson.Lesson import Lesson


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


    def import_schedule_documents(self, use_classrooms: bool):
        """
        Imports a csv of a schedule into a list of Lesson objects and Gang (class) objects

        :return: a list with a list Classroom objects and a list of Gang objects
        """
        classroom_dict = {}
        for classroom in self.classroom_list:
            classroom_dict[classroom.name] = classroom
        schedule = []
        gang_list = []
        create_gang = True
        for root, dirs, files in os.walk(self.input_path):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_path, file)
                    f = open(file_to_open, 'r', encoding="utf8")
                    csvreader = csv.reader(f)
                    next(csvreader)

                    for row in csvreader:
                        if row[5] and row[6] and row[8]:
                            lesson = Lesson(row[0], row[1], row[2], row[3],
                                            int(row[4]), row[5], row[6], row[7], row[8], row[9])

                            if not use_classrooms or not row[10] or row[10] not in classroom_dict.keys():
                                schedule.append((lesson, None))
                            else:
                                classroom_dict[row[10]].set_unavailable(lesson.generate_time_blocks())
                                schedule.append((lesson, classroom_dict[row[10]]))

                            for gang in gang_list:
                                if gang.name == lesson.gang:  # TODO tratar de várias turmas para a mesma Lesson
                                    gang.add_lesson(lesson)
                                    create_gang = False
                                    break
                            if create_gang:
                                gang_list.append(Gang(lesson.gang, lesson.course, lesson))
                            else:
                                create_gang = True
                    f.close()
        return gang_list, schedule

    def import_classrooms(self):
        """
        Imports a csv into a list of Classroom objects

        :return: list of Classroom objects
        """
        char_rarity = {}
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
                        for ch in charact_list:
                            if ch in char_rarity.keys():
                                char_rarity[ch] += 1
                            else:
                                char_rarity[ch] = 1
                        self.classroom_list.append(classroom)
                    f.close()
        sorted_char_rarity = sorted(char_rarity, key=char_rarity.get, reverse=True)
        sorted_dict = {}
        for w in sorted_char_rarity:
            sorted_dict[w] = char_rarity[w]
        return self.classroom_list, sorted_dict

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



# fazer sempre o import_classrooms antes do import_schedule_documents
mn = Manipulate_Documents(input_path="../input_documents", input_classrooms="../input_classrooms")
mn.import_classrooms()
mn.import_schedule_documents(True)

