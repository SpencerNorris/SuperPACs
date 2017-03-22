FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD run.sh /
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN apt-get install libmysqlclient-dev
RUN pip install -r src/requirments.txt
RUN chmod +x /code/run.sh
#CMD ["/code/run.sh"]
CMD ["man ssh"]