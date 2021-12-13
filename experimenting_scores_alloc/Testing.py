from experimenting_scores_alloc.JMP_andre import JMP_andre
from file_manager.Manipulate_Documents import Manipulate_Documents
from jmetalpy.JMP import JMP
from metrics.Metric import Overbooking, Underbooking, BadClassroom, RoomlessLessons

md = Manipulate_Documents("../input_documents", "../output_documents", "../input_classrooms")
gangs, l = md.import_schedule_documents("Exemplo_de_horario_primeiro_semestre.csv", False)
classrooms = md.import_classrooms()
metrics = [RoomlessLessons(), Overbooking(), Underbooking(), BadClassroom()]
# metrics = [Overbooking()]
lessons = [le[0] for le in l]
JMP_andre().run_algorithm("floatnsgaii", lessons, classrooms, metrics)
