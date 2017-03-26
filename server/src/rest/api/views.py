from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


'''

basic view that returns on basic http://localhost:8000/api/ call.

'''
def index(request):
    return HttpResponse("<h2> This works!!!!!!!</h2>")
