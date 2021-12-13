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
import io
from lesson.Lesson import *

def index(request):
    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
def results(request):
    if request.method == 'POST' and request.FILES['filename']:
        myFile = request.FILES['filename']
        #f = myFile.read().decode('utf-8')
        myFile.seek(0)
        #csvreader = csv.DictReader(io.StringIO(myFile.read().decode('utf-8')))
        #print(f)
        #dialect = csv.Sniffer().sniff(codecs.EncodedFile(myFile,"utf-8").read(1024))
        #f.open() # seek to 0
        #csvreader = csv.reader(codecs.EncodedFile(myFile,"utf-8"),
        #                        dialect=dialect)
        #f = codecs.EncodedFile(request.FILES['filename'],"utf-8")
        csvreader = csv.reader(io.StringIO(myFile.read().decode('utf-8')))
        lesson_list = []
        gang_list = []
        create_gang = True
        #for root, dirs, files in os.walk(self.input_path):
        #    for file in files:
        #        if file.endswith(tuple(self.ext)):
        #            file_to_open = os.path.join(self.input_path, file)
        #            f = open(file_to_open, 'r', encoding="utf8")
        next(csvreader)
        for row in csvreader:
            print(row)
            lesson = Lesson(row[0], row[1], row[2], row[3], int(row[4]), row[5], row[6], row[7], row[8], row[9])
            lesson_list.append(lesson)
            for gang in gang_list:
                if gang.name == lesson.gang: # TODO tratar de várias turmas para a mesma Lesson
                    gang.add_lesson(lesson)
                    create_gang = False
                    break
            if create_gang:
                gang_list.append(Gang(lesson.gang, lesson.course, lesson))
            else:
                create_gang = True
        myFile.close()
        print (lesson_list)
        
        fs = FileSystemStorage()
        #filename = fs.save('\tmp\Input_Documents', myFile)
        #uploaded_file_url = fs.url(filename)
        manipulate_docs = Manipulate_Documents()
        lessons, ganga  = manipulate_docs.import_schedule_documents()
        classes = manipulate_docs.import_classrooms()
        
        try:
            os.mkdir(os.path.join('/app', '/tmp/'))
        except Exception:
            print("didnt create dir")
        print(request.POST.get("degree"))
        #filename = fs.save('/app/tmp', myFile)
        #app.config['UPLOAD_FOLDER'] = "/tmp/"
        #filename = send_from_directory("/tmp/", myFile)
        a = Allocator(classes,lessons,ganga)
        a.lessons = [l for l in a.lessons if l.start]
        '''for lesson in lessons:
            a.add_lesson(lesson)'''
        #for classroom in classes:
        #    a.add_classroom(classroom)

        #schedule = a.simple_allocation()
        #filename = open("/app/tmp/Exemplo_de_horario_do_1o_Semestre.csv", "w")
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
        
        # content of all algorithms to show on page, append to render
        return render(request, 'results.html', {"context": context,"table_headers": headers})

        #return render(request, 'results.html', {"context": context,"table_headers": headers, "myFile": filename})

    return render(request, 'index.html')
    #return HttpResponse(s.nice())
    
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