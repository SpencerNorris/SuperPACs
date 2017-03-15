
from django.conf.urls import url,include
from . import views
'''
basic self-referencing controller.
'''
urlpatterns = [
    url(r'$', views.index),
]
