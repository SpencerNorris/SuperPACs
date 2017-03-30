from datasource import fec
from datasource import propublica
import os


FEC_APIKEY = os.getenv('FEC_API_KEY', '')
ProPublica_APIKEY = os.getenv('PP_API_KEY', '')

def donations():
    print(FEC_APIKEY)
    FecApiObj = fec.FECAPI(FEC_APIKEY)
    committees = FecApiObj.get_committees()
    print(len(committees))
    PPCampFinObj = propublica.CampaignFinanceAPI(ProPublica_APIKEY)
    PPCongressApi = propublica.CongressAPI(ProPublica_APIKEY)
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
            indepExpend = PPCampFinObj.get_indep_expends(str(committee['committee_id']))
            if(count%100==0):
                #print(expend['candidate_name']+" "+count)
                print("committee ",count," ",str(committee['committee_id']))

            #if(len(donations)>0):
            #    return donations

            for expend in indepExpend["results"]:
                if(expend['candidate_name'] in legislator_index):
                    #expend fo a particular expenditure
                    expend['committee_id'] = str(committee['committee_id'])
                    expend['propublica_candidate_id'] = str(legislator_index[expend['candidate_name']]['id'])
                    donations.append(expend)
            count += 1
    return donations
