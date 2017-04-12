
import os
import MySQLdb
import django
from api.models import *
from django.core.exceptions import MultipleObjectsReturned
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
restpath = srcpath+"/rest"

os.sys.path.append(restpath)

from fec import *
from propublica import *
from parse_indepexpends import *



ProPublica_APIKEY = os.getenv('PP_API_KEY', '')
FEC_APIKEY = os.getenv('FEC_API_KEY', '')
##abstract base class for
class AbstractSeeder:

    def __init__(self):
        ##Django environment
        os.environ['DJANGO_SETTINGS_MODULE'] = 'rest.settings'
        ##api keys
        self.ProPublica_APIKEY = ""
        self.FEC_API_KEY = ""

        ##Find out way to pass in the testing or production database to seed.
        ##Unfortunately, it is currently based on the environment where this seeder object is called.


    ##function skeletons.
    '''
    Gets all the representatives straight from the API into a JSON form
    that the uploadRepresentatives() function can ingest
    '''
    @staticmethod
    def getRepresentatives():
        pass
    '''
    Accepts a representative JSON list and puts it into the django ORM.
    '''
    def uploadRepresentatives(self,representatives_list):
        pass

    '''
    Gets all the SuperPACs straight from the API into a JSON form
    that the uploadSuperPACs() function can ingest
    '''
    @staticmethod
    def getSuperPACs():
        pass
    '''
    Accepts a superpac JSON list and puts it into the django ORM.
    '''
    def uploadSuperPACs(self,superpacs_list):
        pass

    '''
    Gets all the donations straightfrom the API into a JSON form
    that the uploadDonations() function can ingest
    '''
    @staticmethod
    def getDonations():
        pass
    '''
    Accepts a donations JSON list and puts it into the django ORM.
    '''
    def uploadDonations(self,donations_list):
        pass

    '''
    calls all functions here, to get all json, and upload it to the ORM.
    '''
    def seedAll():
        pass
class UploaderSeeder(AbstractSeeder):
    def __init__(self):
        AbstractSeeder.__init__(self)

    def uploadRepresentatives(self,congress_list):
        for congressman in congress_list["house"]['results'][0]['members']:
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

        for senator in congress_list["senate"]['results'][0]['members']:
            senator_dict = {}#personal details
            senator_dict["propublicaid"] = senator['id']
            senator_dict["first_name"] = senator['first_name']
            senator_dict["last_name"] = senator['last_name']
            #office details
            senator_dict["state"] = senator['state']
            senator_dict["party"] = senator['party']
            senator_dict["chamber"] = "S"

            Representative.objects.create(**senator_dict)

    def uploadSuperPACs(self,superpac_list):
        for superpac in superpacs_list:
            superpac_dict = {}
            superpac_dict["name"]=superpac["name"]
            superpac_dict["fecid"]=superpac["committee_id"]
            SuperPAC.objects.create(**superpac_dict)

    def uploadDonations(self,donation_list):
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

class APISeeder(UploaderSeeder):
    def __init__(self):
        UploaderSeeder.__init__(self)

    @staticmethod
    def getRepresentatives():
        ##get all the representatives in json
        con_obj = CongressAPI(apikey=ProPublica_APIKEY,congressnum=115)
        house_list = con_obj.list_members(chamber = "house")
        senators_list = con_obj.list_members(chamber = "senate")

        congress_list = {}
        congress_list["house"] = house_list
        congress_list["senate"] = senate_list
        return congress_list

    @staticmethod
    def getSuperPACs():
        fec_obj = FECAPI(FEC_APIKEY)
        superpacs_list = fec_obj.get_committees()
        return superpacs_list

    @staticmethod
    def getDonations():
        donation_list = donations_helper()
        return donation_list



    def seedAll(self):
        reps_list = getRepresentatives()
        uploadRepresentatives(reps_list)

        superpacs_list = getSuperPACs()
        uploadSuperPACs(superpacs_list)

        donations_list = getDonations()
        uploadDonations(donations_list)



class PickleSeeder(UploaderSeeder):

    def __init__(self):
        UploaderSeeder.__init__(self)
        ##pickled, cached data
        self.donations_pickle_filename="donationdata.pickle"
        self.superpacs_pickle_filename="superpacdata.pickle"
        self.representative_pickle_filename="representativedata.pickle"

    def getRepresentatives(self):
        try:
            print("superpac data pickled already. Grabbing data from representativedata.picke")
            return APISeeder.getRepresentatives()
        except EOFError:
            print("representative data not pickled, grabbing directly from FEC and ProPublica APIs")
            donations = donations_helper()

            with open(self.representative_pickle_filename, 'wb') as handle:
                pickle.dump(donations, handle, protocol=pickle.HIGHEST_PROTOCOL)

            return donations

    def getSuperPACs(self):
        try:
            print("superpac data pickled already. Grabbing data from superpacdata.picke")
            return APISeeder.getSuperPACs()
        except EOFError:
            print("superpac data not pickled, grabbing directly from FEC and ProPublica APIs")
            donations = donations_helper()

            with open(self.superpacs_pickle_filename, 'wb') as handle:
                pickle.dump(donations, handle, protocol=pickle.HIGHEST_PROTOCOL)

            return donations

    def getDonations(self):
        try:
            print("donation data pickled already. Grabbing data from donationdata.picke")
            return APISeeder.getDonations()
        except EOFError:
            print("donation data not pickled, grabbing directly from FEC and ProPublica APIs")
            donations = donations_helper()

            with open(self.donations_pickle_filename, 'wb') as handle:
                pickle.dump(donations, handle, protocol=pickle.HIGHEST_PROTOCOL)

            return donations

    def seedAll(self):
        #Check if we have a pickle ready?

        reps_list = APISeeder.getRepresentatives()
        self.uploadRepresentatives(reps_list)

        superpacs_list = APISeeder.getSuperPACs()
        self.uploadSuperPACs(superpacs_list)

        donations_list = APISeeder.getDonations()
        self.uploadDonations(donations_list)

def uploadToDatabase():
    apiseeder = APISeeder()
    apiseeder.seedAll()

'''
def uploadToDatabase(picklefilename):
    Donation.objects.all().delete()
    print("Deleting all donations")

    Representative.objects.all().delete()
    print("Deleting all representatives.")

    SuperPAC.objects.all().delete()
    print("Deleting all SuperPACs.")


    representative_json = uploadRepresentatives()
    print("Finished seeding Representatives.")

    superpac_json = uploadSuperPACs()
    print("Finished seeding SuperPACs.")

    donation_json = uploadDonations(picklefilename)
    print("Finished seeding Donations.")
'''

if __name__ == "__main__":
    django.setup()
    from api.models import *

    uploadToDatabase()
