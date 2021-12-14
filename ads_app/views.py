import mimetypes
from os import read
import sys

from django.shortcuts import render
from operator import itemgetter
from cytoolz import take

from django.http import HttpResponse, FileResponse
from file_manager.Manipulate_Documents import *
from alocate.Allocator import *
from metrics import Metric
from metrics.Metric import Gaps, UsedRooms, RoomlessLessons, Overbooking, Underbooking, BadClassroom, RoomMovements, \
    BuildingMovements, ClassroomInconsistency
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404
import json
import io
from lesson.Lesson import *
import copy


def index(request):
    return render(request, 'index.html')
    # return HttpResponse(s.nice())


def results(request):
    if request.method == 'POST' and request.FILES['filename']:
        mp = Manipulate_Documents()
        myFile = request.FILES['filename']
        myFile.seek(0)
        gang_list, schedule = mp.import_schedule_documents(myFile, False)
        metrics_chosen = request.POST.getlist('metrics')
        all_metrics = ["RoomlessLessons", "Overbooking", "Underbooking", "BadClassroom", "Gaps", "RoomMovements", "BuildingMovements", "UsedRooms", "ClassroomInconsistency"]
        metrics = []
        metrics_jmp_compatible = []
        for metric in metrics_chosen:
            if metric == "RoomlessLessons":
                metrics.append(RoomlessLessons())
                metrics_jmp_compatible.append(RoomlessLessons())
            if metric == "Overbooking":
                metrics.append(Overbooking())
                metrics_jmp_compatible.append(Overbooking())
            if metric == "Underbooking":
                metrics.append(Underbooking())
                metrics_jmp_compatible.append(Underbooking())
            if metric == "BadClassroom":
                metrics.append(BadClassroom())
                metrics_jmp_compatible.append(BadClassroom())
            if metric == "Gaps":
                metrics.append(Gaps())
            if metric == "RoomMovements":
                metrics.append(RoomMovements())
            if metric == "BuildingMovements":
                metrics.append(BuildingMovements())
            if metric == "UsedRooms":
                metrics.append(UsedRooms())
            if metric == "ClassroomInconsistency":
                metrics.append(ClassroomInconsistency())
                    
                    
                    

        # myFile = request.FILES['filename']
        ##f = myFile.read().decode('utf-8')
        # myFile.seek(0)
        # print(type(myFile))
        ##csvreader = csv.DictReader(io.StringIO(myFile.read().decode('utf-8')))
        ##print(f)
        ##dialect = csv.Sniffer().sniff(codecs.EncodedFile(myFile,"utf-8").read(1024))
        ##f.open() # seek to 0
        ##csvreader = csv.reader(codecs.EncodedFile(myFile,"utf-8"),
        ##                        dialect=dialect)
        ##f = codecs.EncodedFile(request.FILES['filename'],"utf-8")
        # csvreader = csv.reader(io.StringIO(myFile.read().decode('utf-8')))
        # print(type(csvreader))
        # lesson_list = []
        # gang_list = []
        # create_gang = True
        # for root, dirs, files in os.walk(self.input_path):
        #    for file in files:
        #        if file.endswith(tuple(self.ext)):
        #            file_to_open = os.path.join(self.input_path, file)
        #            f = open(file_to_open, 'r', encoding="utf8")
        # next(csvreader)
        # for row in csvreader:
        #    print(row)
        #    lesson = Lesson(row[0], row[1], row[2], row[3], int(row[4]), row[5], row[6], row[7], row[8], row[9])
        #    lesson_list.append(lesson)
        #    for gang in gang_list:
        #        if gang.name == lesson.gang: # TODO tratar de várias turmas para a mesma Lesson
        #            gang.add_lesson(lesson)
        #            create_gang = False
        #            break
        #    if create_gang:
        #        gang_list.append(Gang(lesson.gang, lesson.course, lesson))
        #    else:
        #        create_gang = True
        # myFile.close()
        # print (lesson_list)
        #
        # fs = FileSystemStorage()
        ##filename = fs.save('\tmp\Input_Documents', myFile)
        ##uploaded_file_url = fs.url(filename)
        # manipulate_docs = Manipulate_Documents()
        # lessons, ganga  = manipulate_docs.import_schedule_documents()
        classrooms = mp.import_classrooms()

        # try:
        #    os.mkdir(os.path.join('/app', '/tmp/'))
        # except Exception:
        #    print("didnt create dir")
        # print(request.POST.get("degree"))
        # filename = fs.save('/app/tmp', myFile)
        # app.config['UPLOAD_FOLDER'] = "/tmp/"
        # filename = send_from_directory("/tmp/", myFile)
        
        #metrics = [RoomlessLessons(), Overbooking(), Underbooking(), BadClassroom()]
        c_copy = copy.deepcopy(classrooms)
        g_copy = copy.deepcopy(gang_list)
        s_copy = copy.deepcopy(schedule)
        a_simple = Allocator(c_copy, s_copy, g_copy, metrics)
        a_jmp = Allocator(c_copy, s_copy, g_copy, metrics_jmp_compatible)

        print("\nsimple_allocation:\n")

        start = time.time()

        simple_schedule = a_simple.simple_allocation()

        elapsed_time = time.time() - start
        
        results_metrics = {"Metric":[],"Algorithm - Simple":[],"Algorithm - Weekly":[], "Algorithm - Overbooking": []};
        for m in metrics:
            m.calculate(simple_schedule)
            print(m.name, ": ", round(m.get_percentage() * 100, 2), "%")
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Simple"].append(round(m.get_percentage() * 100, 2))


        #room_metric = RoomlessLessons()
        #room_metric.calculate(simple_schedule)
        #
        #overbooking_metric = Overbooking()
        #overbooking_metric.calculate(simple_schedule)
        #
        #underbooking_metric = Underbooking()
        #underbooking_metric.calculate(simple_schedule)
        #
        #bad_classroom_metric = BadClassroom()
        #bad_classroom_metric.calculate(simple_schedule)
        #
        #gaps_metric = Gaps()
        #gaps_metric.calculate(simple_schedule)
        #
        #room_movements_metric = RoomMovements()
        #room_movements_metric.calculate(simple_schedule)
        #
        #building_movements_metric = BuildingMovements()
        #building_movements_metric.calculate(simple_schedule)
        #
        #used_rooms_metric = UsedRooms()
        #used_rooms_metric.calculate(simple_schedule)
        #
        #classroom_inconsistency_metric = ClassroomInconsistency()
        #classroom_inconsistency_metric.calculate(simple_schedule)

        #print("Roomless Lessons Percentage:", round(room_metric.get_percentage() * 100, 2), "%")
        #print("Overbooking Percentage:", round(overbooking_metric.get_percentage() * 100, 2), "%")
        #print("Underbooking Percentage:", round(underbooking_metric.get_percentage() * 100, 2), "%")
        #print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage() * 100, 2), "%")
        #print("Gaps Percentage:", round(gaps_metric.get_percentage() * 100, 2), "%")
        #print("Room Movement Percentage:", round(room_movements_metric.get_percentage() * 100, 2), "%")
        #print("Building movement Percentage:", round(building_movements_metric.get_percentage() * 100, 2), "%")
        #print("Used Rooms Percentage:", round(used_rooms_metric.get_percentage() * 100, 2), "%")
        #print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2),
        #      "%")
        print("Elapsed time: ", elapsed_time, "\n")

        a_simple.remove_all_allocations()

        print("\nallocation_with_overbooking:\n")

        start = time.time()

        lessons30 = a_simple.weekly_allocation()

        elapsed_time = time.time() - start

        tamanho = sys.getsizeof(lessons30)

        start_convert = time.time()
        schedule_andre = []
        for sublist in lessons30.values():
            for item in sublist:
                schedule_andre.append(item)
        elapsed_time_convert = time.time() - start_convert

        start_metricas = time.time()

        for m in metrics:
            m.calculate(schedule_andre)
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Weekly"].append(round(m.get_percentage() * 100, 2))
       
        #room_metric = RoomlessLessons()
        #room_metric.calculate(schedule_andre)
        #
        #overbooking_metric = Overbooking()
        #overbooking_metric.calculate(schedule_andre)
        #
        #underbooking_metric = Underbooking()
        #underbooking_metric.calculate(schedule_andre)
        #
        #bad_classroom_metric = BadClassroom()
        #bad_classroom_metric.calculate(schedule_andre)
        #
        #elapsed_time_metricas = time.time() - start_metricas
        #
        #print("\n\nandre_algorithm:\n")
        #print("Roomless Lessons Percentage:", round(room_metric.get_percentage(), 2) * 100, "%")
        #print("Overbooking Percentage:", round(overbooking_metric.get_percentage(), 2) * 100, "%")
        #print("Underbooking Percentage:", round(underbooking_metric.get_percentage(), 2) * 100, "%")
        #print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage(), 2) * 100, "%")
        #
        #print("Elapsed time: ", elapsed_time)
        #print("Elapsed time on metricas: ", elapsed_time_metricas)
        #print("Elapsed time on convert: ", elapsed_time_convert)
        #print("Tamanho do lessons30: ", tamanho)

        a_jmp.remove_all_allocations()
        allocation_with_overbooking = a_jmp.allocation_with_overbooking(30)

        elapsed_time = time.time() - start

        schedule_nuno = []
        for sublist in allocation_with_overbooking.values():
            for item in sublist:
                schedule_nuno.append(item)

        for m in metrics_jmp_compatible:
            m.calculate(schedule_nuno)
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Overbooking"].append(round(m.get_percentage() * 100, 2))
            
        #room_metric = RoomlessLessons()
        #room_metric.calculate(schedule_nuno)
        #
        #overbooking_metric = Overbooking()
        #overbooking_metric.calculate(schedule_nuno)
        #
        #underbooking_metric = Underbooking()
        #underbooking_metric.calculate(schedule_nuno)
        #
        #bad_classroom_metric = BadClassroom()
        #bad_classroom_metric.calculate(schedule_nuno)
        #
        #gaps_metric = Gaps()
        #gaps_metric.calculate(schedule_nuno)
        #
        #room_movements_metric = RoomMovements()
        #room_movements_metric.calculate(schedule_nuno)
        #
        #building_movements_metric = BuildingMovements()
        #building_movements_metric.calculate(schedule_nuno)
        #
        #used_rooms_metric = UsedRooms()
        #used_rooms_metric.calculate(schedule_nuno)
        #
        #classroom_inconsistency_metric = ClassroomInconsistency()
        #classroom_inconsistency_metric.calculate(schedule_nuno)
        #
        #print("Roomless Lessons Percentage:", round(room_metric.get_percentage() * 100, 2), "%")
        #print("Overbooking Percentage:", round(overbooking_metric.get_percentage() * 100, 2), "%")
        #print("Underbooking Percentage:", round(underbooking_metric.get_percentage() * 100, 2), "%")
        #print("Bad Classroom Percentage:", round(bad_classroom_metric.get_percentage() * 100, 2), "%")
        #print("Gaps Percentage:", round(gaps_metric.get_percentage() * 100, 2), "%")
        #print("Room Movement Percentage:", round(room_movements_metric.get_percentage() * 100, 2), "%")
        #print("Building movement Percentage:", round(building_movements_metric.get_percentage() * 100, 2), "%")
        #print("Used Rooms Percentage:", round(used_rooms_metric.get_percentage() * 100, 2), "%")
        #print("Classroom Inconsistency Percentage:", round(classroom_inconsistency_metric.get_percentage() * 100, 2),
        #      "%")
        #print("Elapsed time: ", elapsed_time, "\n")

        '''for lesson in lessons:
            a.add_lesson(lesson)'''
        # for classroom in classes:
        #    a.add_classroom(classroom)

        # schedule = a.simple_allocation()
        # filename = open("/app/tmp/Exemplo_de_horario_do_1o_Semestre.csv", "w")
        # data = output_file.read()
        # object.save()
        # context = upload.objects.all()
        # request.FILES['filename'] = manipulate_docs.export_schedule(schedule, "Output_Schedule")
        # return render(request, 'results.html', {"context": output_file})
        for key, val in results_metrics.items():
            print(key, " ", val)
        # table columns
        headers = {"Metric": "Metrics", "Algorithm - Simple": "Algorithm - Simple", "Algorithm - Weekly": "Algorith - Weekly", "Algorithm - Overbooking": "Algorithm - Overbooking"}

        # content of evaluation table
        context = [{"Metric": "1", "Algorithm - 1": "97.5%", "Algorithm - 2": "50%"},
                   {"Metric": "2", "Algorithm - 1": "10.5%", "Algorithm - 2": "99.7%"}]
        context = json.dumps(context)
        results_metrics = json.dumps(results_metrics)
        # content of all algorithms to show on page, append to render
        return render(request, 'results.html', {"context": context, "table_headers": headers, "results_metrics": results_weekly})

        # return render(request, 'results.html', {"context": context,"table_headers": headers, "myFile": filename})

    return render(request, 'index.html')
    # return HttpResponse(s.nice())


def download_file(request):
    # fill these variables with real values
    # fl_path = "Output_Documents/"
    # filename = 'Output_Schedule.csv'
    lines = ["test"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=Algorithm_Results.csv'
    response.writelines(lines)
    return response