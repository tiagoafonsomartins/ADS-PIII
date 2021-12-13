import mimetypes
from os import read

from django.shortcuts import render

from django.http import HttpResponse, FileResponse
from file_manager.Manipulate_Documents import *
from alocate.Allocator import *
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404
import json


def index(request):
    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
def results(request):
    if request.method == 'POST' and request.FILES['filename']:
            myFile = request.FILES['filename']
            fs = FileSystemStorage()
            #filename = fs.save('\tmp\Input_Documents', myFile)
            #uploaded_file_url = fs.url(filename)
            manipulate_docs = Manipulate_Documents()
            lessons, ganga  = manipulate_docs.import_schedule_documents()
            classes = manipulate_docs.import_classrooms()
            try:
                os.mkdir(os.path.join('/app', '/tmp/'))
            except Exception:
                
            filename = fs.save('/app/tmp', myFile)
            #app.config['UPLOAD_FOLDER'] = "/tmp/"
            #filename = send_from_directory("/tmp/", myFile)
            a = Allocator(classes,lessons,ganga)
            a.lessons = [l for l in a.lessons if l.start]
            '''for lesson in lessons:
                a.add_lesson(lesson)'''
            #for classroom in classes:
            #    a.add_classroom(classroom)

            #schedule = a.simple_allocation()
            filename = open("/app/tmp/Exemplo_de_horario_do_1o_Semestre.csv", "w")
            #data = output_file.read()
            #object.save()
            #context = upload.objects.all()
            #request.FILES['filename'] = manipulate_docs.export_schedule(schedule, "Output_Schedule")
            #return render(request, 'results.html', {"context": output_file})
            
            # table columns
            headers = {"Metric": "Metric", "Algorithm - 1": "Algorithm - 1", "Algorithm - 2": "Algorithm - 2"}
            
            # content of evaluation table
            context = [{"Metric": "1", "Algorithm - 1": "97.5%", "Algorithm - 2" : "50%"},{"Metric": "2", "Algorithm - 1": "10.5%", "Algorithm - 2" : "99.7%"}]
            context = json.dumps(context)
            
            return render(request, 'results.html', {"context": context,"table_headers": headers, "myFile": filename})
    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
def download_file(request):
    # fill these variables with real values
    fl_path = "Output_Documents/"
    filename = 'Output_Schedule.csv'

    response = HttpResponse(open("Output_Documents\Output_Schedule.csv", 'rb').read())
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=DownloadedText.csv'
    return response