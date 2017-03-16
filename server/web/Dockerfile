FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD code /code/
RUN apt-get install libmysqlclient-dev
RUN pip install -r src/requirements.txt
RUN ls -al .
