import os
import MySQLdb
import django
from api.models import *
from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction
from time import sleep
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
restpath = srcpath+"/rest"

os.sys.path.append(restpath)

from fec import *
from propublica import *
from parse_indepexpends import *



ProPublica_APIKEY = os.getenv('PP_API_KEY', '')
FEC_APIKEY = os.getenv('FEC_API_KEY', '')
##abstract base class for the seeder class.
##has getter functions, which get the data from any source for the data contract that the ORM accepts
    ####getter functions can have different implementation
    #### in APISeeder(UploaderSeeder(AbstractSeeder)), the data comes straight from the API. the function is static too.
    #### in PickleSeeder(UploaderSeeder(AbstractSeeder)), the data comes from a cached "pickle" data
    ##### However, if the pickle files do not exist, or the data is wrong, or if you just want to get a new batch of data
    ##### PickleSeeder's getter functions will call APISeeder's getter functions, and will then set it into a new pickle.
##has uploader functions, which sends the data to the ORM.
##those are implemented in UploaderSeeder(AbstractSeeder), and don't really change much.

class AbstractSeeder:

    def __init__(self):
        ##Django environment
        os.environ['DJANGO_SETTINGS_MODULE'] = 'rest.settings'
        ##api keys
        self.ProPublica_APIKEY = ""
        self.FEC_API_KEY = ""

        ##Find out way to pass in the testing or production database to seed.
        ##Unfortunately, it is currently based on the environment where this seeder object is called.

    ##TODO: Should I add a place here to delete parts of the database?

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

            ##Simple try catch block to avoid duplicate congressman problems
            with transaction.atomic():
                ##Django 1.5/1.6 transaction bug requires above check
                try:
                    Representative.objects.create(**congress_dict)
                except django.db.utils.IntegrityError:
                    pass

        for senator in congress_list["senate"]['results'][0]['members']:
            senator_dict = {}#personal details
            senator_dict["propublicaid"] = senator['id']
            senator_dict["first_name"] = senator['first_name']
            senator_dict["last_name"] = senator['last_name']
            #office details
            senator_dict["state"] = senator['state']
            senator_dict["party"] = senator['party']
            senator_dict["chamber"] = "S"

            ##Simple try catch block to avoid duplicate senator problems
            with transaction.atomic():
                ##Django 1.5/1.6 transaction bug requires above check
                try:
                    Representative.objects.create(**senator_dict)
                except django.db.utils.IntegrityError:
                    pass


    def uploadSuperPACs(self,superpac_list):
        for superpac in superpac_list:
            superpac_dict = {}
            superpac_dict["name"]=superpac["name"]
            superpac_dict["fecid"]=superpac["committee_id"]

            ##Simple try catch block to avoid duplicate superpac problems
            with transaction.atomic():
                ##Django 1.5/1.6 transaction bug requires above check
                try:
                    SuperPAC.objects.create(**superpac_dict)
                except django.db.utils.IntegrityError:
                    pass


    def uploadDonations(self,donation_list):
        print("database congress size:",len(Representative.objects.all()))
        for donation in donation_list:
            donation_dict = {}

            rep = Representative.objects.get(propublicaid=donation["propublica_candidate_id"])
            sup = SuperPAC.objects.get(fecid=donation["committee_id"])

            donation_dict["representative_id"] = rep.id
            donation_dict["superpac_id"] = sup.id
            donation_dict["amount"] = donation["amount"]
            donation_dict["uid"] = donation["unique_id"]
            donation_dict["support"] = donation["support_or_oppose"]

            ##Simple try catch block to avoid duplicate donation problems
            with transaction.atomic():
                ##Django 1.5/1.6 transaction bug requires above check
                try:
                    Donation.objects.create(**donation_dict)
                except django.db.utils.IntegrityError:
                    pass

class APISeeder(UploaderSeeder):
    def __init__(self):
        UploaderSeeder.__init__(self)

    @staticmethod
    def getRepresentatives():
        ##get all the representatives in json
        con_obj = CongressAPI(apikey=ProPublica_APIKEY,congressnum=115)
        house_list = con_obj.list_members(chamber = "house")
        senate_list = con_obj.list_members(chamber = "senate")

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
        print("APISeeder seeding starting.")

        print("getting representatives")
        representatives_list = self.getRepresentatives()
        self.uploadRepresentatives(representatives_list)
        print("finished uploading representatives")

        print("getting superpacs")
        superpacs_list = self.getSuperPACs()
        self.uploadSuperPACs(superpacs_list)
        print("finished uploading superpacs")

        print("getting donations")
        donations_list = self.getDonations()
        self.uploadDonations(donations_list)
        print("finished uploading donations")



class PickleSeeder(UploaderSeeder):

    def __init__(self):
        UploaderSeeder.__init__(self)
        ##pickled, cached data

        self.representatives_pickle_filename="../datasource/pickles/representativedata.pickle"
        self.superpacs_pickle_filename="../datasource/pickles/superpacdata.pickle"
        self.donations_pickle_filename="../datasource/pickles/donationdata.pickle"

        ##Where to put the file for refreshing the pickled data?

    ##call APISeeder method for getting data, and then pickle it in the class file for it.
    def pickleRepresentatives(self):
        print("Pickling Representatives from APISeeder.")
        representatives_list = APISeeder.getRepresentatives()
        with open(self.representatives_pickle_filename, 'wb') as handle:
            pickle.dump(representatives_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return representatives_list

    def getRepresentatives(self):
        #Check for time-sensitive reasons to not use cache? Or perhaps use a subclass..
        try:
            try:
                ##pull data from the pickle.
                with open(self.representatives_pickle_filename, 'rb') as handle:
                    representatives_list = pickle.load(handle)
                print("superpac data pickled already. Grabbing data from "+self.representatives_pickle_filename)
            except FileNotFoundError:
                print("No "+self.representatives_pickle_filename+" file. Creating file from APISeeder data.")
                ##seed the pickle if the file doesn't exist
                representatives_list = self.pickleRepresentatives()

            return representatives_list
        except EOFError:
            print("representative data not pickled, grabbing directly from FEC and ProPublica APIs")
            representatives_list = self.pickleRepresentatives()
            ##seed the pickle if the file exists but has weird data.

            return representatives_list

    ##call APISeeder method for getting data, and then pickle it in the class file for it.
    def pickleSuperPACs(self):
        print("Pickling SuperPACs from APISeeder.")
        superpacs_list = APISeeder.getSuperPACs()
        with open(self.superpacs_pickle_filename, 'wb') as handle:
            pickle.dump(superpacs_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return superpacs_list

    def getSuperPACs(self):
        try:
            try:
                ##pull data from the pickle.
                with open(self.superpacs_pickle_filename, 'rb') as handle:
                    superpacs_list = pickle.load(handle)
                print("superpac data pickled already. Grabbing data from "+self.superpacs_pickle_filename)
            except FileNotFoundError:
                print("No "+self.superpacs_pickle_filename+" file. Creating file from APISeeder data.")
                ##seed the pickle if the file doesn't exist
                superpacs_list = self.pickleSuperPACs()

            return superpacs_list
        except EOFError:
            print("superpac data not pickled, grabbing directly from FEC and ProPublica APIs")
            superpacs_list = self.pickleSuperPACs()
            ##seed the pickle if the file exists but has weird data.

            return superpacs_list

    ##call APISeeder method for getting data, and then pickle it in the class file for it.
    def pickleDonations(self):
        print("Pickling Donations from APISeeder.")
        donations_list = APISeeder.getDonations()
        with open(self.donations_pickle_filename, 'wb') as handle:
            pickle.dump(donations_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return donations_list

    def getDonations(self):
        try:
            try:
                ##pull data from the pickle.
                with open(self.donations_pickle_filename, 'rb') as handle:
                    donations_list = pickle.load(handle)
                print("donation data pickled already. Grabbing data from "+self.donations_pickle_filename)
            except FileNotFoundError:
                print("No "+self.donations_pickle_filename+" file. Creating file from APISeeder data.")
                ##seed the pickle if the file doesn't exist
                donations_list = self.pickleDonations()
            return donations_list

        except EOFError:
            print("donation data not pickled, grabbing directly from FEC and ProPublica APIs")
            ##seed the pickle if the file exists but has weird data.

            donations_list = self.pickleDonations()
            return donations_list

    def seedAll(self,reset=False):
        ##Check if the previous pickle has been updated in the past 24 hours?
        ##Or should I delegate this to a subclass.
        ##anyways, the optional reset keyword will re-call the api seeder operations, to delete the pickles and replace them

        if not reset:
            representatives_list = self.getRepresentatives()
            self.uploadRepresentatives(representatives_list)

            superpacs_list = self.getSuperPACs()
            self.uploadSuperPACs(superpacs_list)

            donations_list = self.getDonations()
            self.uploadDonations(donations_list)
        else:
            representatives_list = self.pickleRepresentatives()
            self.uploadRepresentatives(representatives_list)

            superpacs_list = self.pickleSuperPACs()
            self.uploadSuperPACs(superpacs_list)

            donations_list = self.pickleDonations()
            self.uploadDonations(donations_list)


#this is only necessary when seeding the database when deploying the application, not in tests.
def uploadToDatabase():
    Donation.objects.all().delete()
    print("Deleting all donations")
    Representative.objects.all().delete()
    print("Deleting all representatives.")
    SuperPAC.objects.all().delete()
    print("Deleting all SuperPACs.")


    seeder = PickleSeeder()
    print("Using Pickle seeder to get data.")
    seeder.seedAll(reset=False)


if __name__ == "__main__":
    django.setup()
    from api.models import *
    print("starting main function:")
    uploadToDatabase()
