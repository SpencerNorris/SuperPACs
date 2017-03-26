# Django

## Django Documentation
https://docs.djangoproject.com/en/1.10/

## Django Project file structure
http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

## Django Setup

(Make this better)


/src/rest/
$ python3 manage.py runserver
Runs the django server onto localhost:8000

/src/rest/rest/
$ export DJANGO_SECRET_KEY="password"
sets environment variable for the django secret key, is referenced in /src/rest/rest/settings.py
now > SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default_value) will be "password"

### Migrations: models.py ORM to sql schema
https://docs.djangoproject.com/en/1.10/topics/migrations/
Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.

What we want to do is get the /api/models.py ORM class representation into a mysql database schema so that we can add to it from the caching APIs.

From

$ cd server/src/rest

1. Create your ORM model: in our case, api/models.py
2. Make a migration,
  - $ python3 manage.py makemigrations
3. Send that migration to the mysql server you specified in rest/settings.py
  - $ python3 manage.py migrate
4. Open mysql database from settings.py
5. Notice that we now have a schema representing the models.py


## Django Comments

Django forces you to do things the Django way, because its usually the right way to do things.

If you want customization, you can do it all yourself, but it will devolve into spaghetti code fast.

rest: Name of the django app, it contains sub apps, the main one being /rest/, and the rest api of the app is called /api/.

You are supposed to divide the parts of your web app into "individual web apps"

## Django File Explanation

For each sub-app, (/rest/, /api/), it contains many required files:
__init__.py: Tells python that this folder is a "package".
settings.py: Configuration settings,,,
urls.py: Binds url endpoints to views.
wsgi.py:(main app only): deployment file,,,
views.py: Takes a request(from urls.py binding), and returns a view. Accesses models.py to get information.
models.py: An ORM representation of the data classes, which links to a database. Each class has methods for accessing/modifying/deleting data.
