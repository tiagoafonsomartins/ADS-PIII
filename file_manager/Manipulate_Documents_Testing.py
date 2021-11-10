from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from lesson.Lesson import Lesson


class Manipulate_Documents_Testing:

    def __init__(self):
        pass

    def test_export_schedule(self):
        schedule = [(Lesson("MEI", "ADS", "69420blz", "t-69", 69, "Sex", "3:00:00", "10:00:00", "4/23/2005", "Good, Not stinky, Very good"), Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Auditório 4', 250, 125, ["cenas", "mais cenas"])),
                    (Lesson("LEI", "PCD", "69420blzit", "t-420", 420, "Qui", "3:00:00", "10:00:00", "12/23/2005", "Good, Not stinky"), Classroom('Edifício 2', 'B203', 250, 125, ["cenas", "mais cenas", "ainda mais cenas"])),
                    (Lesson("ETI", "Irrelevant stuff", "42069blz", "t-1337", 420, "Sex", "3:00:00", "10:00:00", "4/06/2005", "Good, Very good"), Classroom('Edifício 69', 'Auditório 420', 250, 125, ["cenas"])),
                    (Lesson("MEI", "GSI", "4269blzit", "t-69", 42069, "Sex", "3:00:00", "10:00:00", "9/14/2015", "Not stinky, Very good"), Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Auditório 4', 250, 125, ["cenas", "mais cenas", "outras cenas"])),
                    (Lesson("MEI", "SRSI", "Ya drenas", "t-69", 420, "Qua", "3:00:00", "10:00:00", "5/31/2069", "Not stinky"), Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Sala daquelas tipo fixes', 250, 125, ["cenas", "mais cenas"]))]
        MD = Manipulate_Documents(output_path="..\\Output_Testing_Documents")
        MD.export_schedule(schedule, "testingExport")
        MD.export_schedule(schedule, "*?!$:=")
        MD.export_schedule([], "moreTesting")

    def test_list_to_comma_sep_string(self):
        MD = Manipulate_Documents(output_path="..\\Output_Testing_Documents")
        print(MD.list_to_comma_sep_string(["Hello", "How are you", "I'm fine"]))
        print(MD.list_to_comma_sep_string([]))
        print(MD.list_to_comma_sep_string([1,2,3]))
        print(MD.list_to_comma_sep_string([[1,2,3], 5.7, (1,2,3), {"hello":1, "what":2}]))

MDT = Manipulate_Documents_Testing()
MDT.test_export_schedule()
MDT.test_list_to_comma_sep_string()





