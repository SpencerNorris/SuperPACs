FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD run.sh /
RUN mkdir /code
WORKDIR /code
ADD code /code/
RUN apt-get install libmysqlclient-dev
RUN pip install -r src/requirements.txt
RUN chmod +x /run.sh
CMD ["/run.sh"]
