# Django

## Django Documentation
https://docs.djangoproject.com/en/1.10/

## Django Project file structure
http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

## Django Setup

(Make this better)

/src/rest/
$ django-admin.py startproject rest
Created the main django environment

/src/rest/
$ python3 manage.py runserver
Runs the django server onto localhost:8000

/src/rest/rest/
$ python3 manage.py startapp rest
Creates the app rest


## Django Comments

Django forces you to do things the Django way, because its usually the right way to do things.

If you want customization, you can do it all yourself, but it will devolve into spaghetti code fast.

rest: Name of the django app, it contains sub apps, the main one being /rest/, and the rest api of the app is called /restapi/.

You are supposed to divide the parts of your web app into "individual web apps"

## Django File Explanation

For each sub-app, (/rest/, /restapi/), it contains many required files:
__init__.py: Tells python that this folder is a "package".
settings.py: Configuration settings,,,
urls.py: Binds url endpoints to views.
wsgi.py:(main app only): deployment file,,,
views.py: Takes a request(from urls.py binding), and returns a view. Accesses models.py to get information.
models.py: An ORM representation of the data classes, which links to a database. Each class has methods for accessing/modifying/deleting data.
