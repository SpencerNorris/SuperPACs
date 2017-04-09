"""
File: datasource\methodtests.py
Author: Kevin Reitano
Description:
"""

from ..\datasource import propublica
from ..\datasource import fec


def testfec_get_committees(apikey=None):
    """
    Tests the FEC API method for getting getting committees
    :param apikey: The FEC API key
    :return: True if test passes, False otherwise
    """
    if apikey is None:
        print("No FEC API key provided")
        return False
    fecobj = fec.FECAPI(apikey)
    try:
        res = fecobj.get_committees()
        if('contains' not in res[0]):
            print('For FEC Api, the method "get_committees" result does not include cycles')
            return False
        if('committee_id' not in res[0]):
            print('For FEC Api, the method "get_committees" result does not include committee_id')
            return False
    except:
        print('For FEC Api, the method "get_committees" failed')
        return False
    return True

def testpp_list_members(apikey='None'):
    """
    Tests the ProPublica Congress API method for getting members of the house and senate
    :param apikey: The ProPublica API key
    :return: True if test passes, False otherwise
    """
    if apikey is None:
        print("No ProPublica API key provided")
        return False
    congobj = propublica.CongressApi(apikey)
    try:
        resHouse = congobj.list_members('house')
        resSenate = congobj.list_members('senate')
        if('members' not in resHouse[0] or 'members' not in resSenate[0]):
            print('For ProPublica Congress Api, the method "list_members" result does not include members')
            return False
        if('first_name' not in resHouse['results'][0] or 'first_name' not in resSenate['results'][0]):
            print('For ProPublica Congress Api, the method "list_members" result does not include first_name')
            return False
        if ('last_name' not in resHouse['results'][0] or 'last_name' not in resSenate['results'][0]):
            print('For ProPublica Congress Api, the method "list_members" result does not include last_name')
            return False
    except:
        print('For ProPublica Congress Api, the method "list_members" failed')
        return False
    return True

def testpp_get_indep_expends(apikey=None):
    """
    Tests the ProPublica Campaign Finance API method for getting independant expenditures
    :param apikey: The ProPublica API key
    :return: True if test passes, False otherwise
    """
    if apikey is None:
        print("No ProPublica API key provided")
        return False
    campfinobj = propublica.CampaignFinanceApi(apikey)
    try:
        res = campfinobj.get_indep_expends('C00607275')
        if('committee_id' not in res["results"][0]):
            print('For ProPublica Congress Api, the method "committee_id" result does not include committee_id')
            return False
        if('propublica_candidate_id' not in res['results'][0]):
            print('For ProPublica Congress Api, the method "list_members" result does not include propublica_candidate_id')
            return False
    except:
        print('For ProPublica Congress Api, the method "get_indep_expends" failed')
        return False
    return True