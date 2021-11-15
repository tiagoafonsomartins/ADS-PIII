from os import read

from django.shortcuts import render

from django.http import HttpResponse, FileResponse
from file_manager.Manipulate_Documents import *
from alocate.Allocator import *
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
def results(request):
    if request.method == 'POST' and request.FILES['filename']:
            myFile = request.FILES['filename']
            fs = FileSystemStorage()
            filename = fs.save('Input_Documents', myFile)
            #uploaded_file_url = fs.url(filename)
            manipulate_docs = Manipulate_Documents()
            lessons = manipulate_docs.import_schedule_documents()
            classes = manipulate_docs.import_classrooms()
            
            a = Allocator()
            for lesson in lessons:
                a.add_lesson(lesson)
            for classroom in classes:
                a.add_classroom(classroom)

            schedule = a.simple_allocation()
            output_file = open("Output_Documents\Output_Schedule.csv")
            request.FILES['file2'] = output_file
            #object.save()
            #context = upload.objects.all()
            request.FILES['filename'] = manipulate_docs.export_schedule(schedule, "Output_Schedule")
            return render(request, 'results.html', {"context": output_file})
            #response = FileResponse(open(filename, 'rb'))
            #return render(response, 'results.html')
    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
def importFile(request):
    if request.method == 'POST' and request.FILES['filename']:
            myFile = request.FILES['filename']
            fs = FileSystemStorage()
            filename = fs.save('Input_Documents', myFile)
            #uploaded_file_url = fs.url(filename)
            manipulate_docs = Manipulate_Documents()
            lessons = manipulate_docs.import_schedule_documents()
            classes = manipulate_docs.import_classrooms()
            
            a = Allocator()
            for lesson in lessons:
                a.add_lesson(lesson)
            for classroom in classes:
                a.add_classroom(classroom)

            schedule = a.simple_allocation()

            
            response = FileResponse(open(filename, 'rb'))
            return render(response, 'results.html')
            #request.FILES['myFile'] = md.export_schedule(schedule, "Output_Schedule")
            #return render(request, 'results.html')
            
    return render(request, 'index.html')