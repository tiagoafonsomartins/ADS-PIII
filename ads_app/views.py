import mimetypes
from os import read
import sys

from django.shortcuts import render, redirect
from operator import itemgetter
from cytoolz import take  #

from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.urls import reverse

from alocate.overbooking_with_jmp_algorithm import overbooking_with_jmp_algorithm
from alocate.simple_allocation import simple_allocation
from alocate.weekly_allocation import weekly_allocation
from file_manager.Manipulate_Documents import *
from lang_dict.Lang_Dict import Lang_Dict
from metrics import Metric
from metrics.Metric import Gaps, UsedRooms, RoomlessLessons, Overbooking, Underbooking, BadClassroom, RoomMovements, \
    BuildingMovements, ClassroomInconsistency
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404
import json
import io
# from lesson.Lesson import *
import copy

from metrics.Metric import RoomlessLessons, Overbooking

global schedule_simple
global schedule_overbooking
global chosen_language
chosen_language = "en"


def index(request):
    global chosen_language
    chosen_language
    page_dict = Lang_Dict(chosen_language)
    # print(page_dict.dictionary["home"])
    return render(request, 'index.html', {"context": "context", "page_dict": page_dict.dictionary})


def choose_language(request):
    global chosen_language

    chosen_language = request.POST.get("chosen_language")
    page_dict = Lang_Dict(chosen_language)
    # chosen_language = "pt"
    # redirect_to = reverse('', kwargs={"context": "context", "page_dict": page_dict.dictionary})
    # return redirect(redirect_to)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'),
                                {"context": "context", "page_dict": page_dict.dictionary})


def results(request):
    global chosen_language
    chosen_language
    page_dict = Lang_Dict(chosen_language)
    if request.method == 'POST' and request.FILES['filename']:
        mp = Manipulate_Documents()
        myFile = request.FILES['filename']
        db_metrics = []

        '''DownloadSimple
        DownloadWeekly
        DownloadOverbooking
        SelectSimple
        SelectWeekly
        SelectOverbooking'''
        myFile.seek(0)
        schedule = mp.import_schedule_documents(myFile, False)
        metrics_chosen = request.POST.getlist('metrics')
        metrics = []
        metrics_jmp_compatible = []
        for metric in metrics_chosen:
            if metric == "RoomlessLessons":
                metrics.append(RoomlessLessons())
                metrics_jmp_compatible.append(RoomlessLessons())
                db_metrics.append('metric_RoomlessLessons')
            if metric == "Overbooking":
                metrics.append(Overbooking())
                metrics_jmp_compatible.append(Overbooking())
                db_metrics.append('metric_Overbooking')
            if metric == "Underbooking":
                metrics.append(Underbooking())
                metrics_jmp_compatible.append(Underbooking())
                db_metrics.append('metric_Underbooking')
            if metric == "BadClassroom":
                metrics.append(BadClassroom())
                metrics_jmp_compatible.append(BadClassroom())
                db_metrics.append('metric_BadClassroom')
            if metric == "Gaps":
                metrics.append(Gaps())
                db_metrics.append('metric_Gaps')
            if metric == "RoomMovements":
                metrics.append(RoomMovements())
                db_metrics.append('metric_RoomMovements')
            if metric == "BuildingMovements":
                metrics.append(BuildingMovements())
                db_metrics.append('metric_BuildingMovements')
            if metric == "UsedRooms":
                metrics.append(UsedRooms())
                db_metrics.append('metric_UsedRooms')
            if metric == "ClassroomInconsistency":
                metrics.append(ClassroomInconsistency())
                db_metrics.append('metric_ClassroomInconsistency')

        classrooms = mp.import_classrooms()

        c_copy = copy.deepcopy(classrooms)

        s_copy = copy.deepcopy(schedule)
        a_simple = simple_allocation(s_copy, c_copy)

        c_copy = copy.deepcopy(classrooms)
        s_copy = copy.deepcopy(schedule)
        a_weekly = weekly_allocation(s_copy, c_copy)

        c_copy = copy.deepcopy(classrooms)
        s_copy = copy.deepcopy(schedule)

        if not request.POST.get("Overbooking_max"):
            a_jmp = overbooking_with_jmp_algorithm(s_copy,
                                                   c_copy,
                                                   metrics_jmp_compatible)
        else:
            a_jmp = overbooking_with_jmp_algorithm(s_copy,
                                                   c_copy,
                                                   metrics_jmp_compatible,
                                                   int(request.POST.get("Overbooking_max")))

        results_metrics = {"Metric Description": [],
                           "Metric": [],
                           "Algorithm - Simple": [],
                           "Algorithm - Weekly": [],
                           "Algorithm - Overbooking": []}
        i = 0
        for m in metrics:
            m.calculate(a_simple)
            results_metrics["Metric Description"].append(page_dict.dictionary[db_metrics[i]])
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Simple"].append(str(round(m.get_percentage() * 100, 2)) + "%")
            m.reset_metric()
            i += 1

        schedule_andre = []
        for sublist in a_weekly.values():
            for item in sublist:
                schedule_andre.append(item)

        i = 0
        for m in metrics:
            m.calculate(schedule_andre)
            results_metrics["Metric Description"].append(page_dict.dictionary[db_metrics[i]])
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Weekly"].append(str(round(m.get_percentage() * 100, 2)) + "%")
            m.reset_metric()
            i += 1

        schedule_nuno = []
        for sublist in a_jmp.values():
            for item in sublist:
                schedule_nuno.append(item)

        i = 0
        for m in metrics:
            m.calculate(schedule_nuno)
            results_metrics["Metric Description"].append(page_dict.dictionary[db_metrics[i]])
            results_metrics["Metric"].append(m.name)
            results_metrics["Algorithm - Overbooking"].append(str(round(m.get_percentage() * 100, 2)) + "%")
            m.reset_metric()
            i += 1

        iterator = len(results_metrics["Algorithm - Simple"])
        i = 0
        final_dict = []
        while i < iterator:
            tmp_dict = {}
            for key, values in results_metrics.items():
                # print(tmp_dict[key], "inside for", values[i])
                try:
                    tmp_dict[key] = values[i]
                except Exception:
                    print("didn't insert the value")

            final_dict.append(tmp_dict)
            i += 1
        results_metrics = final_dict

        # a_simple represents the schedule from the simple algorithm
        # schedule_nuno represents the schedule from the overbooking algorithm
        global schedule_simple
        global schedule_overbooking
        global schedule_weekly
        # get
        schedule_simple = a_simple
        schedule_overbooking = schedule_nuno
        schedule_weekly = schedule_andre
        # table columns
        headers = {"Metric Description": str(page_dict.dictionary["MetricDescription"]),
                   "Metric": str(page_dict.dictionary["Metric"]),
                   "Algorithm - Simple": str(page_dict.dictionary["algorithm_simple"]),
                   "Algorithm - Weekly": str(page_dict.dictionary["algorithm_weekly"]),
                   "Algorithm - Overbooking": str(page_dict.dictionary["algorithm_overbooking"])}

        # content of evaluation table
        context = [{"Metric": "1",
                    "Algorithm - 1": "97.5%",
                    "Algorithm - 2": "50%"},
                   {"Metric": "2",
                    "Algorithm - 1": "10.5%",
                    "Algorithm - 2": "99.7%"}]
        context = json.dumps(context)
        results_metrics = json.dumps(results_metrics)
        # content of all algorithms to show on page, append to render
        return render(request, 'results.html',
                      {"context": context,
                       "table_headers": headers,
                       "results_metrics": results_metrics,
                       "page_dict": page_dict.dictionary,
                       })

    return render(request, 'index.html', {"page_dict": page_dict.dictionary})


def download_file(request):
    # fill these variables with real values
    # fl_path = "Output_Documents/"
    # filename = 'Output_Schedule.csv'
    global schedule_simple
    global schedule_overbooking
    global schedule_weekly
    global chosen_language
    page_dict = Lang_Dict(chosen_language)
    filename = ""
    if request.method == 'POST':
        if request.POST.get("algorithm") == "simple_algorithm":
            filename = page_dict.dictionary["DownloadSimple"]
            lines = Manipulate_Documents().export_schedule_str(schedule_simple)
        if request.POST.get("algorithm") == "weekly_algorithm":
            filename = page_dict.dictionary["DownloadWeekly"]
            lines = Manipulate_Documents().export_schedule_str(schedule_weekly)
        if request.POST.get("algorithm") == "overbooking_algorithm":
            filename = page_dict.dictionary["DownloadOverbooking"]
            lines = Manipulate_Documents().export_schedule_str(schedule_overbooking)
        response = HttpResponse(content_type='text/csv')
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'

        content = ""
        for x in lines:
            content += x + "\n"
        response.writelines(content)

    return response


if __name__ == '__main__':
    ld = choose_language("pt")
