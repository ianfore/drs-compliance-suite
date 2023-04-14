# base image
FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# set python path to current dir
ENV PYTHONPATH /usr/src/app

RUN pip3 install -r requirements.txt

# run the command
ENTRYPOINT ["python","compliance_suite/report_runner.py"]