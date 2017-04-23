from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F, Sum, Value
from django.db.models.functions import Concat

from api.models import Representative,SuperPAC,Donation

import re
import requests
import json
import os

srcpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.sys.path.append(srcpath)
from datasource.sunlight import SunlightAPI
from datasource.propublica import CongressAPI

ProPublica_APIKEY = os.getenv('PP_API_KEY', '')

def index(request):
    '''
    basic view that returns on basic http://localhost:8000/api/ call.
    '''
    return HttpResponse("<h2> This works!!!!!!!</h2>")

def demo(request):
    '''
    example data from our api
    '''
    return JsonResponse({ "representatives": { "1": { "id": 1, "name": "Nancy Pelosi", "party": "d" }, "2": { "id": 2, "name": "Paul Ryan", "party": "r" }, "3": { "id": 3, "name": "Rick Scott", "party": "r" } }, "committees": { "1": { "id": 1, "name": "Guns for Americans" }, "2": { "id": 2, "name": "Right to Rise" }, "3": { "id": 3, "name": "Pro Life PAC" } }, "bills": { "1": { "id": 1, "name": "Club Baby Seal Act of 2017" }, "2": { "id": 2, "name": "Dirty Water Act" }, "3": { "id": 3, "name": "No More Handouts Act" } }, "donations": [ { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 1, "amount": 100 }, { "from": 1, "to": 2, "amount": 300 }, { "from": 2, "to": 2, "amount": 700 }, { "from": 2, "to": 3, "amount": 50 }, { "from": 3, "to": 1, "amount": 200 }, { "from": 3, "to": 3, "amount": 400 } ], "votes": [ { "from": 1, "to": 1, "pass": "true" }, { "from": 1, "to": 2, "pass": "false" }, { "from": 1, "to": 3, "pass": "false" }, { "from": 2, "to": 1, "pass": "true" }, { "from": 2, "to": 2, "pass": "true" }, { "from": 2, "to": 3, "pass": "true" }, { "from": 3, "to": 1, "pass": "false" }, { "from": 3, "to": 2, "pass": "true" }, { "from": 3, "to": 3, "pass": "false" } ] })

def donations(request):
    '''
    actual data from the FEC, propublica data, through the django ORM cache
    '''
    data = {}

    data["representatives"] = {d["id"]: d for d in
        Representative.objects.all()
            .annotate(name=Concat('first_name', Value(" "), 'last_name'))
            .values("id", "name", "party","state","district")}

    data["committees"] = {d["id"]: d for d in
        SuperPAC.objects.all().values("id", "name")}

    data["donations"] = list(Donation.objects.all()
        .annotate(source=F("superpac_id"), destination=F("representative_id"))
        .values("source", "destination", "support")
        .annotate(amount=Sum("amount")))

    return JsonResponse(data)

def donationsDemo(request):
    '''
    actual data from the FEC, propublica data, through the django ORM cache
    this returns specially selected pieces of data for demo purposes
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

    data["donations"] = list(Donation.objects.all()
        .annotate(source=F("superpac_id"), destination=F("representative_id"))
        .values("source", "destination", "support")
        .annotate(amount=Sum("amount")))

    return JsonResponse(data)

def search(request):
    '''
    Searches through all available sources to match the user's query
    '''
    query = request.GET["query"]

    ## match the query against a zipcode regex, go a zipcode search if it matches
    if re.match("^\d{5}$", query):
        ## here we call an external api to search for the reps via zipcode
        results = SunlightAPI().rep_by_zip(query)

        ## loop through the results
        reps = []
        for rep in results["results"]:
            ## try finding the rep in our database
            reps += (Representative.objects.all()
                .annotate(name=Concat('first_name', Value(" "), 'last_name'))
                .filter(name=rep["first_name"]+" "+rep["last_name"])
                .values("id", "name", "party"))
        ## return the found reps
        return JsonResponse({"representatives": reps, "committees": []})

    data = {}

    data["representatives"] = list(Representative.objects.all()
        .annotate(name=Concat('first_name', Value(" "), 'last_name'))
        .filter(name__icontains=query)
        .values("id", "name", "party"))

    data["committees"] = list(SuperPAC.objects.filter(name__icontains=query)
        .values("id", "name"))

    if "." in query or len(query) > 5:
        results = SunlightAPI().search(query)
        data["bills"] = results["results"]

    return JsonResponse(data)

def votes(request):
    '''
    Returns votes for the given bill
    '''
    bill_id = request.GET["bill_id"]

    #get latest roll call vote from sunlight
    results = SunlightAPI().votes(bill_id)
    print(results)
    if len(results["results"]) == 0:
        return JsonResponse({"votes": []})

    last_vote = results["results"][0]

    #get individual votes for the roll call vote
    results = CongressAPI(ProPublica_APIKEY).get_vote(last_vote["congress"], last_vote["chamber"], 2-last_vote["year"]%2, last_vote["number"])

    data = {"votes": []}

    for vote in results["results"]["votes"]["vote"]["positions"]:
        rep = Representative.objects.filter(propublicaid=vote["member_id"]).first()
        if rep is not None:
            data["votes"].append({"source": rep.id, "destination": bill_id, "position": vote["vote_position"]})

    return JsonResponse(data)
