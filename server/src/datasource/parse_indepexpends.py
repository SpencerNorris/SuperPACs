from datasource import fec
from datasource import propublica
import os


FEC_APIKEY = os.getenv('FEC_API_KEY', '')
ProPublica_APIKEY = os.getenv('PP_API_KEY', '')

FecApiObj = fec.FECAPI(FEC_APIKEY)
committees = FecApiObj.get_committees()
PPCampFinObj = propublica.CampaignFinanceAPI(ProPublica_APIKEY)
PPCongressApi = propublica.CongressAPI(ProPublica_APIKEY)
legislator_index = list()
legislators = PPCongressApi.list_members('house')["results"][0]["members"]
for legislator in legislators:
    name = str(legislator['first_name']) + " " + str(legislator['last_name'])
    legislator_index.append(name)
legislators = PPCongressApi.list_members('senate')["results"][0]["members"]
for legislator in legislators:
    name = str(legislator['first_name']) + " " + str(legislator['last_name'])
    legislator_index.append(name)


for committee in committees:
    if(2016 in committee['cycles']):
        indepExpend = PPCampFinObj.get_indep_expends(str(committee['committee_id']))
        for expend in indepExpend["results"]:
            if(expend['candidate_name'] in legislator_index):
                #expend fo a particular expenditure
