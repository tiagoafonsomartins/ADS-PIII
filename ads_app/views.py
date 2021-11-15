from django.shortcuts import render

from django.http import HttpResponse
from file_manager.Manipulate_Documents import *
from django.shortcuts import render

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
            for classroom in classrooms:
                a.add_classroom(classroom)

            schedule = a.simple_allocation()

            
            response = FileResponse(open(filename, 'rb'))
            return render(response)
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
            for classroom in classrooms:
                a.add_classroom(classroom)

            schedule = a.simple_allocation()

            
            response = FileResponse(open(filename, 'rb'))
            return render(response)
            #request.FILES['myFile'] = md.export_schedule(schedule, "Output_Schedule")
            #return render(request, 'results.html')
            
    return render(request, 'index.html')