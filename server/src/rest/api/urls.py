
from django.conf.urls import url,include
from . import views
'''
basic self-referencing controller.
'''
urlpatterns = [
    url(r'^$', views.index),
    url(r'^demo$', views.demo),
    url(r'^donations$', views.donations),
    url(r'^donationsDemo$', views.donationsDemo),
    url(r'^search$', views.search),
    url(r'^votes$', views.votes)
]
