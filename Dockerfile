# Install the base requirements for the app.
# This stage is to support development.
#FROM python:alpine AS base
#WORKDIR /app
COPY requirements.txt .
#RUN pip install -r requirements.txt
RUN pip install -r requirements.txt

FROM python:3
WORKDIR /ADS-PIII
COPY ADS-PIII/experiments.py ADS-PIII/db.sqlite3 ADS-PIII/experiments.py ADS-PIII/runtime.txt ADS-PIII/requirements.txt ADS-PIII/Procfile ADS-PIII/manage.py ADS-PIII/main.py ./
COPY ADS-PIII/ads_app ./ads_app
COPY ADS-PIII/alocate ./alocate
COPY ADS-PIII/classroom ./classroom
COPY ADS-PIII/django_ads ./django_ads
COPY ADS-PIII/file_manager ./file_manager
COPY ADS-PIII/gang ./gang
COPY ADS-PIII/input_classrooms ./input_classrooms
COPY ADS-PIII/input_documents ./input_documents
COPY ADS-PIII/lesson ./lesson
COPY ADS-PIII/media ./media
COPY ADS-PIII/metrics ./metrics
COPY ADS-PIII/output_documents ./output_documents
COPY ADS-PIII/output_testing_documents ./output_testing_documents
COPY ADS-PIII/lesson ./lesson
COPY ADS-PIII/lesson ./lesson
COPY ADS-PIII/lesson ./lesson

# Run tests to validate app
#FROM app-base AS test
#RUN apk add --no-cache python3 g++ make
#RUN yarn install
#RUN yarn test


## Clear out the node_modules and create the zip
#FROM app-base AS app-zip-creator
#COPY app/package.json app/yarn.lock ./
#COPY app/spec ./spec
#COPY app/src ./src
#RUN apk add zip && \
#    zip -r /app.zip /app
#
## Dev-ready container - actual files will be mounted in
#FROM base AS dev
#CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
#
## Do the actual build of the mkdocs site
#FROM base AS build
#COPY . .
#RUN mkdocs build
#
## Extract the static content from the build
## and use a nginx image to serve the content
#FROM nginx:alpine
#COPY --from=app-zip-creator /app.zip /usr/share/nginx/html/assets/app.zip
#COPY --from=build /app/site /usr/share/nginx/html
