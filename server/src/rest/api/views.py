from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from api.models import Representative,SuperPAC,Donation
#from rest.api.models.representative import representative

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


def restdemo(request):
    '''
    better data
    '''

    return JsonResponse({ "representatives": { "1": { "id": 1, "name": "Nancy Pelosi", "party": "d" }, "2": { "id": 2, "name": "Paul Ryan", "party": "r" }, "3": { "id": 3, "name": "Rick Scott", "party": "r" } }, "committees": { "1": { "id": 1, "name": "Guns for Americans" }, "2": { "id": 2, "name": "Right to Rise" }, "3": { "id": 3, "name": "Pro Life PAC" } }, "bills": { "1": { "id": 1, "name": "Club Baby Seal Act of 2017" }, "2": { "id": 2, "name": "Dirty Water Act" }, "3": { "id": 3, "name": "No More Handouts Act" } }, "donations": [ { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 2, "amount": 300 }, { "from": 2, "to": 2, "amount": 700 }, { "from": 2, "to": 3, "amount": 50 }, { "from": 3, "to": 1, "amount": 200 }, { "from": 3, "to": 3, "amount": 400 } ], "votes": [ { "from": 1, "to": 1, "pass": "true" }, { "from": 1, "to": 2, "pass": "false" }, { "from": 1, "to": 3, "pass": "false" }, { "from": 2, "to": 1, "pass": "true" }, { "from": 2, "to": 2, "pass": "true" }, { "from": 2, "to": 3, "pass": "true" }, { "from": 3, "to": 1, "pass": "false" }, { "from": 3, "to": 2, "pass": "true" }, { "from": 3, "to": 3, "pass": "false" } ] })

def datademo(request):
    '''
    actual data from the FEC, propublica data, through the django ORM cache
    '''
    data = {"representatives":{},"committees":{},"donations":[]}
    representative_list = Representative.objects.all()
    special_reps = [488,200,390,119,49,445,491]
    for rep in representative_list:
        if rep.first_name+" "+rep.last_name in ['Ted Cruz','Marco Rubio','Tammy Duckworth','Rand Paul','Ruben Kihuen','Stephanie Murphy']:
            data["representatives"][rep.id] = rep.__json__()

    superpac_list = SuperPAC.objects.all()
    special_pacs = [3505,3498,3453,3323,276]
    for sup in superpac_list:
        if sup.name in ['MAKE DC LISTEN','COURAGEOUS CONSERVATIVES PAC','CONSERVATIVE SOLUTIONS PAC','RIGHT TO RISE USA','NEXTGEN CLIMATE ACTION COMMITTEE','AMERICA\'S LIBERTY PAC','STAND FOR TRUTH','TEXAS TEA PARTY PATRIOTS','FLORIDIANS FOR A STRONG MIDDLE CLASS','HOUSE MAJORITY PAC','PLANNED PARENTHOOD VOTES','IMMIGRANT VOTERS WIN PAC']:
            data["committees"][sup.id] = sup.__json__()

    donation_list = Donation.objects.all()
    for don in donation_list:
        data["donations"].append(don.__json__())



    return JsonResponse(data)
