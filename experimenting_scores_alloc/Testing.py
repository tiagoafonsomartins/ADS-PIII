from file_manager.Manipulate_Documents import Manipulate_Documents
from jmetalpy.JMP import JMP
from metrics.Metric import Overbooking, Underbooking, BadClassroom

md = Manipulate_Documents("../input_documents", "../output_documents", "../input_classrooms")
gangs, l = md.import_schedule_documents(False)
classrooms = md.import_classrooms()
metrics = [Overbooking(), Underbooking(), BadClassroom()]
# metrics = [Overbooking()]
lessons = [le[0] for le in l][:100]

print(JMP().run_algorithm("nsgaii", lessons, classrooms, metrics))
