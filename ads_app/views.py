import mimetypes
from os import read
import sys

from django.shortcuts import render
from operator import itemgetter
from cytoolz import take

from django.http import HttpResponse, FileResponse

from alocate.overbooking_with_jmp_algorithm import overbooking_with_jmp_algorithm
from alocate.simple_allocation import simple_allocation
from alocate.weekly_allocation import weekly_allocation
from file_manager.Manipulate_Documents import *
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

def results(request):
    if request.method == 'POST' and request.FILES['filename']:
        mp = Manipulate_Documents()
        myFile = request.FILES['filename']
        myFile.seek(0)
        schedule = mp.import_schedule_documents(myFile, False)
        metrics_chosen = request.POST.getlist('metrics')
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

        classrooms = mp.import_classrooms()

        c_copy = copy.deepcopy(classrooms)

        s_copy = copy.deepcopy(schedule)
        a_simple = simple_allocation(s_copy, c_copy)

        c_copy = copy.deepcopy(classrooms)
        s_copy = copy.deepcopy(schedule)
        a_weekly = weekly_allocation(s_copy, c_copy)

        c_copy = copy.deepcopy(classrooms)
        s_copy = copy.deepcopy(schedule)

        a_jmp = overbooking_with_jmp_algorithm(int(request.POST.get("Overbooking_weights")), s_copy, c_copy, metrics_jmp_compatible)

        results_metrics = {"Metric":[],"Algorithm - Simple":[],"Algorithm - Weekly":[], "Algorithm - Overbooking": []};
        for m in metrics:
            m.calculate(a_simple)
            print(m.name, ": ", round(m.get_percentage() * 100, 2), "%")
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Simple"].append(str(round(m.get_percentage() * 100, 2)) + "%")

        '''
        schedule_andre = []
        for sublist in a_weekly.values():
            for item in sublist:
                schedule_andre.append(item)


        for m in metrics:
            m.calculate(schedule_andre)
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Weekly"].append(str(round(m.get_percentage() * 100, 2)) + "%")
        '''

        schedule_nuno = []
        for sublist in a_jmp.values():
            for item in sublist:
                schedule_nuno.append(item)

        for m in metrics:
            m.calculate(schedule_nuno)
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Overbooking"].append(str(round(m.get_percentage() * 100, 2)) + "%")

        iterator = len(results_metrics["Algorithm - Simple"])
        i = 0
        final_dict = []
        while i < iterator:
            tmp_dict = {}
            for key, values in results_metrics.items():
                #print(tmp_dict[key], "inside for", values[i])
                try:
                    tmp_dict[key] = values[i]
                except Exception:
                   print("didn't insert the value")

            final_dict.append(tmp_dict)
            i+=1
        results_metrics = final_dict

        #a_simple represents the schedule from the simple algorithm
        #schedule_nuno represents the schedule from the overbooking algorithm

        # table columns
        headers = {"Metric": "Metrics", "Algorithm - Simple": "Algorithm - Simple", "Algorithm - Weekly": "Algorith - Weekly", "Algorithm - Overbooking": "Algorithm - Overbooking"}

        # content of evaluation table
        context = [{"Metric": "1", "Algorithm - 1": "97.5%", "Algorithm - 2": "50%"},
                   {"Metric": "2", "Algorithm - 1": "10.5%", "Algorithm - 2": "99.7%"}]
        context = json.dumps(context)
        results_metrics = json.dumps(results_metrics)
        # content of all algorithms to show on page, append to render
        return render(request, 'results.html', {"context": context, "table_headers": headers, "results_metrics": results_metrics, "simple_algorithm": a_simple, "overbooking_algorithm": schedule_nuno})

    return render(request, 'index.html')

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