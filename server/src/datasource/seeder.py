
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

    #print(congressmen_list['results'][0]['members'][0])
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
        try:
            Representative.objects.create(**congress_dict)
        except django.db.utils.IntegrityError:
            pass
            
    for senator in senators_list['results'][0]['members']:
        senator_dict = {}#personal details
        senator_dict["propublicaid"] = senator['id']
        senator_dict["first_name"] = senator['first_name']
        senator_dict["last_name"] = senator['last_name']
        #office details
        senator_dict["state"] = senator['state']
        senator_dict["party"] = senator['party']
        senator_dict["chamber"] = "S"
        try:
            Representative.objects.create(**senator_dict)
        except django.db.utils.IntegrityError:
            pass

    return True

def uploadSuperPACs():
    fec_obj = FECAPI(FEC_APIKEY)
    superpacs_list = fec_obj.get_committees()

    #print(superpacs_list[0])
    for superpac in superpacs_list:
        #print("Upload: ",superpac["committee_id"])
        superpac_dict = {}
        superpac_dict["name"]=superpac["name"]
        superpac_dict["fecid"]=superpac["committee_id"]
        ##Sometimes the API returns duplicate data, this is a try catch block to avoid it.
        try:
            SuperPAC.objects.create(**superpac_dict)
        except django.db.utils.IntegrityError:
            print("Upload: ",superpac["committee_id"])
            pass


def uploadDonations():
    donation_list = donations()
    print(donation_list[0])
    for donation in donation_list:
        donation_dict = {}

        rep = Representative.objects.get(propublicaid=donation["propublica_candidate_id"])
        sup = SuperPAC.objects.get(fecid=donation["committee_id"])

        donation_dict["representative_id"] = rep.id
        donation_dict["superpac_id"] = sup.id
        donation_dict["amount"] = donation["amount"]
        donation_dict["uid"] = donation["unique_id"]
        donation_dict["support"] = donation["support_or_oppose"]

        ##Sometimes the API returns duplicate data, this is a try catch block to avoid it.
        try:
            Donation.objects.create(**donation_dict)
        except django.db.utils.IntegrityError:
            pass


def uploadToDatabase():

    Representative.objects.all().delete()
    print("Deleting all representatives.")

    representative_json = uploadRepresentatives()
    print("Finished seeding Representatives.")


    SuperPAC.objects.all().delete()
    print("Deleting all SuperPACs.")

    superpac_json = uploadSuperPACs()
    print("Finished seeding SuperPACs.")


    donation_json = uploadDonations()
    print("Finished seeding Donations.")

if __name__ == "__main__":
    django.setup()
    from api.models import *

    uploadToDatabase()
