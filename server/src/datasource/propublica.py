'''
File: datasource/propublica.py
Author: Spencer Norris
Description: Implementation of clients for
the Propublica Campaign Finance and Congress APIs.
'''

from datasource import RESTDatasource
from datasource import APIKeyException
from datasource import URIParameterException


class CampaignFinanceAPI(RESTDatasource):
    def __init__(self, apikey=None):
        """
        The constructor for the CampaignFinanceAPI class
        :param apikey: The ProPublica API key
        """
        # Throw API key errors
        if (apikey is None):
            raise APIKeyException('API key not provided')
        super().__init__(apikey)
        self.uri = "https://api.propublica.org/campaign-finance/v1/"
        self.keyname = 'X-API-Key'


    def get_indep_expends(self, fecid=None, cycle='2016'):
        """
        Gets the independant expenditures for a specific committee for a specific cycle
        :param fecid: The committee's fec id (required)
        :param cycle: The cycle as a string, '2016' is the default
        :return: The results of the api call as json
        """
        if fecid is None:
            raise URIParameterException('FEC ID required but not given')
        params = {}
        headers = {self.keyname: self.apikey}
        requeststr = str(self.uri) + str(cycle) + "/committees/" + str(fecid) + "/independent_expenditures.json"
        return super().request(requeststr, params, headers)

class CongressAPI(RESTDatasource):
    def __init__(self, apikey=None, congressnum='115'):
        """
        Constructor for the CongressAPI class
        :param apikey: The ProPublica API Key
        :param congressnum: The congress number that you want data for, 115 is current as of the 2016 Election cycle
        """
        # Throw API key errors
        if (apikey is None):
            raise APIKeyException('API key not provided')
        super().__init__(apikey)
        self.uri = "https://api.propublica.org/congress/v1/"
        self.keyname = 'X-API-Key'

        #congress number must be 102-115 for House and 80-115 for Senate, 115 is current as of March 2017
        self.congressnum = congressnum


    def set_congressnum(self, newnum):
        """
        Method to change the objects congress number,
        note that congress number must be 102-115 for House and 80-115 for Senate
        :param newnum: The new congressnum for the object
        :return: true if successful, false otherwise
        """
        if newnum > '115' or newnum < '80':
            return False
        else:
            self.congressnum = newnum
            return True


    def list_members(self, chamber=None):
        """
        API Method for getting the list of all members in the House or Senate.
        Uses the congress number given at objects construction
        :param chamber: The chamber of congress you want the members of, either 'house' or 'senate'
        :return: The text of the response for the List of Members api request as json
        """
        if chamber is None:
            raise URIParameterException('Chamber parameter required but not provided')
        requeststr = str(self.uri) + str(self.congressnum) + '/' + str(chamber) + '/members.json'
        rheaders = {self.keyname: self.apikey}
        rparams = {}
        return super().request(requeststr, rparams, rheaders)

    def get_member(self, memberid=None):
        """
        API Method for getting a specific member in the House or Senate
        :param memberid: The member-id of a politician obtained from list_members, consistent with values in
        Biographical Directory of the United States Congress (http://bioguide.congress.gov/biosearch/biosearch.asp)
        :return: The text of the response for the Get Specific Member api request as json
        """
        if memberid is None:
            raise URIParameterException('MemberId parameter required but not provided')
        requeststr = str(self.uri) + str(memberid) + '.json'
        rheaders = {self.keyname: self.apikey}
        rparams = {}
        return super().request(requeststr, rparams, rheaders)


    def get_vote(self, congress, chamber, session, roll_call_number):
        """
        Method for retreiving the breakdown of a specific roll call vote for a piece of legislation.
        :param roll_call_number: the unique identifier for the vote of interest. This is called 'roll_id' by Sunlight.
        :param congress: the numeric identifier for which Congress to retrieve from. The current Congress is '115'.
        :param session: the session of the particular Congress. Pass 1 for the odd-numbered year (e.g. 2013) or 2 for even (2014).
                        This can be determined by the date passed back by Sunlight under 'acted_at'.
        :param chamber: the chamber of Congress the vote is from, either 'house' or 'senate'. This is under the 'chamber' field in Sunlight.
        """
        #All parameters are required!
        if congress is None or chamber is None or session is None or roll_call_number is None:
            raise URIParameterException('MemberId parameter required but not provided') 
        requeststr = str(self.uri) + str(congress) + '/' + chamber + '/sessions/' + str(session) + '/votes/' + str(roll_call_number) + '.json' 
        rheaders = {self.keyname: self.apikey}
        rparams = {}
        return super().request(requeststr, rparams, rheaders)
