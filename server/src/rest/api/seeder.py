
import os
import MySQLdb


os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fec import *
from propublica import *
from parse_indepexpends import *


def uploadRepresentatives(cursor):
    ##get all the representatives in json
    con_obj = CongressAPI(apikey=ProPublica_APIKEY,congressnum=115)
    congressmen_list = con_obj.list_members(chamber = "house")
    senators_list = con_obj.list_members(chamber = "senate")


    #print(congressmen_list)
    return True

def uploadSuperPACs(cursor):
    pass

def uploadDonations(cursor):


    return True


#def uploadBills():
#    pass


def uploadToDatabase():


    cursor = connect(DATABASES['default'])

    representative_json = uploadRepresentatives(cursor)
    superpac_json = uploadSuperPACs(cursor)
    donation_json = uploadDonations(cursor)


    #congressAPI.
    #uploadBills(cursor)
uploadToDatabase()
