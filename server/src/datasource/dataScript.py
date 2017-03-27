from datasource import fec
from datasource import propublica
import os


FEC_APIKEY = os.getenv('FEC_API_KEY', '')
ProPublica_APIKEY = os.getenv('PP_API_KEY', '')

FecApiObj = fec.FECAPI(FEC_APIKEY)
committees = FecApiObj.get_committees()
PPCampFinObj = propublica.CampaignFinanceAPI(ProPublica_APIKEY)
datafile = open("IndepExpends.json", 'w')
for committee in committees:
    if(2016 in committee['cycles']):
        print(committee['committee_id'])
        indepExpend = PPCampFinObj.get_indep_expends(str(committee['committee_id']))
        datafile.write(str(indepExpend))
datafile.close()