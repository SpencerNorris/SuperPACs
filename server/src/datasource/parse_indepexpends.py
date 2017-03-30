import os
srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

restpath = srcpath

os.sys.path.append(restpath)
print(os.sys.path)
from fec import *
from propublica import *
import pickle
from json import JSONDecodeError


FEC_APIKEY = os.getenv('FEC_API_KEY', '')
ProPublica_APIKEY = os.getenv('PP_API_KEY', '')

def donations_helper():
    print(FEC_APIKEY)
    FecApiObj = FECAPI(FEC_APIKEY)
    committees = FecApiObj.get_committees()
    print(len(committees))
    PPCampFinObj = CampaignFinanceAPI(ProPublica_APIKEY)
    PPCongressApi = CongressAPI(ProPublica_APIKEY)
    legislator_index = dict()
    legislators = PPCongressApi.list_members('house')["results"][0]["members"]
    for legislator in legislators:
        name = str(legislator['first_name']) + " " + str(legislator['last_name'])
        legislator_index[name] = legislator
    legislators = PPCongressApi.list_members('senate')["results"][0]["members"]
    for legislator in legislators:
        name = str(legislator['first_name']) + " " + str(legislator['last_name'])
        legislator_index[name] = legislator

    donations = []
    print("committees:",len(committees))
    count = 0
    for committee in committees:
        if(2016 in committee['cycles']):
            try:
                indepExpend = PPCampFinObj.get_indep_expends(str(committee['committee_id']))
                if(count%100==0):
                    #print(expend['candidate_name']+" "+count)
                    print("committee ",count," ",str(committee['committee_id']))

                for expend in indepExpend["results"]:
                    try:
                        #expend fo a particular expenditure
                        expend['committee_id'] = str(committee['committee_id'])
                        expend['propublica_candidate_id'] = str(legislator_index[expend['candidate_name']]['id'])
                        #print(expend)
                        donations.append(expend)
                    except KeyError:
                        pass
            except JSONDecodeError:
                pass
            count += 1
    return donations
def donations():

    try:
        with open('donationdata.pickle', 'rb') as handle:
            donations = pickle.load(handle)
        print("donations",donations)
        return donations
    except EOFError:

        donations = donations_helper()
        #a = {"data":donations,"open":True}

        with open('donationdata.pickle', 'wb') as handle:
            pickle.dump(donations, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("donations",donations)
        return donations
        #pickle.dump(a,open("donationdata.pickle","wb"))


if __name__ == "__main__":

    donations()
