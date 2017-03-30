
import os
import MySQLdb
import django
from django.core.exceptions import MultipleObjectsReturned
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

restpath = srcpath+"/rest"

os.sys.path.append(restpath)
print(restpath)
from fec import *
from propublica import *
from parse_indepexpends import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'rest.settings'

ProPublica_APIKEY = os.getenv('PP_API_KEY', '')
FEC_APIKEY = os.getenv('FEC_API_KEY', '')

def uploadRepresentatives():
    ##get all the representatives in json
    #print(ProPublica_APIKEY)
    con_obj = CongressAPI(apikey=ProPublica_APIKEY,congressnum=115)
    congressmen_list = con_obj.list_members(chamber = "house")
    senators_list = con_obj.list_members(chamber = "senate")

    for congressman in congressmen_list['results'][0]['members']:
        #print(congressman['first_name'])
        congress_dict = {}
        congress_dict["propublicaid"] = congressman['id']
        congress_dict["first_name"] = congressman['first_name']

        #congress_dict["middle_name"] = congressman['middle_name']
        congress_dict["last_name"] = congressman['last_name']
        congress_dict["district"] = congressman['district']
        congress_dict["state"] = congressman['state']
        congress_dict["party"] = congressman['party']
        #congress_dict["in_office"] = bool(congressman['in_office'])
        congress_dict["chamber"] = "H"

        Representative.objects.create(**congress_dict)

    for senator in senators_list['results'][0]['members']:
        #print(senator['first_name'])
        senator_dict = {}
        senator_dict["propublicaid"] = senator['id']
        senator_dict["first_name"] = senator['first_name']

        #senator_dict["middle_name"] = senator['middle_name']
        senator_dict["last_name"] = senator['last_name']
        #senator_dict["district"] = senator['district']
        senator_dict["state"] = senator['state']
        senator_dict["party"] = senator['party']
        #senator_dict["in_office"] = senator['in_office']
        ##somehow in_office is fucky
        senator_dict["chamber"] = "S"

        Representative.objects.create(**senator_dict)

    return True

def uploadSuperPACs():
    fec_obj = FECAPI(FEC_APIKEY)
    superpacs_list = fec_obj.get_committees()

    #print(superpacs_list[0])
    for superpac in superpacs_list:
        superpac_dict = {}
        superpac_dict["name"]=superpac["name"]
        superpac_dict["fecid"]=superpac["committee_id"]
        SuperPAC.objects.create(**superpac_dict)

def uploadDonations():
    donation_list = donations()

    for donation in donation_list:
        donation_dict = {}

        rep = Representative.objects.get(propublicaid=donation["propublica_candidate_id"])
        sup = SuperPAC.objects.get(fecid=donation["committee_id"])

        donation_dict["representative_id"] = rep.id
        donation_dict["superpac_id"] = sup.id
        donation_dict["amount"] = donation["amount"]
        donation_dict["uid"] = donation["unique_id"]
        donation_dict["support"] = donation["support_or_oppose"]
        Donation.objects.create(**donation_dict)
        print("get donation")

        #d = Donation.objects.get(**donation_dict)
        #figure out how to update donation if it already exists.
        '''failed_update = True
        try:
            d = Donation.objects.get(**donation_dict)
            d.uid = donation["unique_id"]
            d.support = donation["support_or_oppose"]
            d.save()
            failed_update = False
            print("old donation save: ",d.amount," ",d.support)
        except MultipleObjectsReturned:
            failed_update = True
            print("new donation: ",d.amount," ",d.support)
        #what if nothing is found!??
        '''
        '''if(d):
            print("new donation save: ",d.amount," ",d.support)
            print(" --> ",donation["support_or_oppose"])
            d.support = donation["support_or_oppose"]
            d.save()
        else:'''




def uploadToDatabase():
    Representative.objects.all().delete()
    representative_json = uploadRepresentatives()
    print("Finished seeding Representatives.")

    SuperPAC.objects.all().delete()
    superpac_json = uploadSuperPACs()
    print("Finished seeding SuperPACs.")
    ##what to do if database already got created.

    donation_json = uploadDonations()
    print("Finished seeding Donations.")

if __name__ == "__main__":
    django.setup()
    from api.models import *

    uploadToDatabase()
