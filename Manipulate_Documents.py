import os


class Manipulate_Documents:

    def __init__(self, input_path="Input_Documents", output_path="Output_Documents",
                 input_classrooms="Input_Classrooms"):
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
        for root, dirs, files in os.walk(self.input_classrooms):
            for file in files:
                if file.endswith(tuple(self.ext)):
                    file_to_open = os.path.join(self.input_classrooms, file)
                    f = open(file_to_open, 'r')
                    print(f.name)
                    # meter nas classes necessárias
                    f.close()


md = Manipulate_Documents()
md.import_classrooms()