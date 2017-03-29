
import os
import MySQLdb
import django

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'superpac'),
        'HOST': 'mysql',
        'PORT': '3306',
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'root')
    }
}

def connect(database):
    '''
    Connecting to the database and returning a cursor.
    '''
    db = MySQLdb.connect(host=database['HOST'],user=database["USER"],passwd=database["PASSWORD"],db=database["NAME"])
    cur = db.cursor()
    return cur


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
    fec_obj = fec.FECAPI(FEC_APIKEY)
    superpacs_list = fec_obj.get_committees()

    print(superpacs_list[0])

def uploadDonations():


    return True


#def uploadBills():
#    pass


def uploadToDatabase():


    #cursor = connect(DATABASES['default'])

    #representative_json = uploadRepresentatives()
    superpac_json = uploadSuperPACs()
    donation_json = uploadDonations()


    #congressAPI.
    #uploadBills(cursor)

if __name__ == "__main__":
    django.setup()
    #import rest.rest.settings
    from api.models import *
    print(1)
    uploadToDatabase()
