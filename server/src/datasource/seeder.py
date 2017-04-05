
import os
import MySQLdb
import django
from django.core.exceptions import MultipleObjectsReturned
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

restpath = srcpath+"/rest"

os.sys.path.append(restpath)

from fec import *
from propublica import *
from parse_indepexpends import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'rest.settings'

ProPublica_APIKEY = os.getenv('PP_API_KEY', '')
FEC_APIKEY = os.getenv('FEC_API_KEY', '')

def uploadRepresentatives():
    ##get all the representatives in json
    con_obj = CongressAPI(apikey=ProPublica_APIKEY,congressnum=115)
    congressmen_list = con_obj.list_members(chamber = "house")
    senators_list = con_obj.list_members(chamber = "senate")

    for congressman in congressmen_list['results'][0]['members']:
        congress_dict = {} #personal details
        congress_dict["propublicaid"] = congressman['id']
        congress_dict["first_name"] = congressman['first_name']
        congress_dict["last_name"] = congressman['last_name']
        #office details
        congress_dict["district"] = congressman['district']
        congress_dict["state"] = congressman['state']
        congress_dict["party"] = congressman['party']
        congress_dict["chamber"] = "H"

        Representative.objects.create(**congress_dict)

    for senator in senators_list['results'][0]['members']:
        senator_dict = {}#personal details
        senator_dict["propublicaid"] = senator['id']
        senator_dict["first_name"] = senator['first_name']
        senator_dict["last_name"] = senator['last_name']
        #office details
        senator_dict["state"] = senator['state']
        senator_dict["party"] = senator['party']
        senator_dict["chamber"] = "S"

        Representative.objects.create(**senator_dict)

    return True

def uploadSuperPACs():
    fec_obj = FECAPI(FEC_APIKEY)
    superpacs_list = fec_obj.get_committees()

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

def uploadToDatabase():

    Representative.objects.all().delete()
    print("Deleting all representatives.")
    print("Using the PP key "+ProPublica_APIKEY)
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
