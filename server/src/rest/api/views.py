from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.


def index(request):
    '''
    basic view that returns on basic http://localhost:8000/api/ call.
    '''
    return HttpResponse("<h2> This works!!!!!!!</h2>")

def demo(request):
	'''
	example data from our api
	'''
    return JsonResponse({"representatives":{"1":{"id":1,"name":"Rep 1","type":"d"},"2":{"id":2,"name":"Rep 2","type":"r"},"3":{"id":3,"name":"Rep 3","type":"r"}},"committees":{"1":{"id":1,"name":"Com 1"},"2":{"id":2,"name":"Com 2"},"3":{"id":3,"name":"Com 3"}},"bills":{"1":{"id":1,"name":"Bill 1"},"2":{"id":2,"name":"Bill 2"},"3":{"id":3,"name":"Bill 3"}},"donations":[{"from":1,"to":1,"amount":100},{"from":1,"to":2,"amount":300},{"from":2,"to":2,"amount":700},{"from":2,"to":3,"amount":50},{"from":3,"to":1,"amount":200},{"from":3,"to":3,"amount":400}],"votes":[{"from":1,"to":1,"pass":True},{"from":1,"to":2,"pass":False},{"from":1,"to":3,"pass":False},{"from":2,"to":1,"pass":True},{"from":2,"to":2,"pass":True},{"from":2,"to":3,"pass":True},{"from":3,"to":1,"pass":False},{"from":3,"to":2,"pass":True},{"from":3,"to":3,"pass":False}]})