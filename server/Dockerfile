FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN apt-get install libmysqlclient-dev
RUN pip install -r src/requirments.txt
CMD ["python", "/code/src/rest/manage.py", "runserver", "0.0.0.0:8000"]
