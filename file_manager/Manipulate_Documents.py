import os

input_path = "../Input_Documents"
output_path = "Output_Documents"
ext = [".csv", ".xml", ".json", ".bd"]

for root, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith(tuple(ext)):
            file_to_open = os.path.join(input_path, file)
            f = open(file_to_open, 'r')
            # meter nas classes necessárias
            f.close()
