# Install the base requirements for the app.
# This stage is to support development.
FROM python:3.9 AS base
WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install OpenJDK-17
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

COPY /experiments.py /db.sqlite3 /experiments.py /runtime.txt /requirements.txt /Procfile /manage.py /main.py ./
COPY /ads_app ./ads_app
COPY /alocate ./alocate
COPY /classroom ./classroom
COPY /django_ads ./django_ads
COPY /file_manager ./file_manager
COPY /input_classrooms ./input_classrooms
COPY /input_documents ./input_documents
COPY /lesson ./lesson
COPY /metrics ./metrics
COPY /output_documents ./output_documents
COPY /output_testing_documents ./output_testing_documents
COPY /lesson ./lesson
COPY /swrlAPI ./swrlAPI
COPY /jmetalpy ./jmetalpy


EXPOSE 8000/tcp
EXPOSE 8000/udp
#FROM django
#RUN python manage.py migrate 
#CMD [ "python", "manage.py runserver 0.0.0.0:8000" ]