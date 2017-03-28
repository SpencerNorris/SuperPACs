"""
-File: datasource/fec.py
-Author: Kevin Reitano
-Description: This File implements the FEC API Wrapper Class
"""

from datasource import RESTDatasource
from datasource import APIKeyException
from datasource import URIParameterException


class FECAPI(RESTDatasource):
    def __init__(self, apikey=None):
        """
        The constructor for the FEC API class
        :param apikey: The FEC Api Key
        """
        # Throw API key errors
        if (apikey is None):
            raise APIKeyException('API key not provided')
        super().__init__(apikey)
        self.uri = "https://api.open.fec.gov/v1/"

    def get_indepexpend(self, committee_id=None, cycle="2016"):
        """
        Function to get independant expenditures of a particular committee for a particular cycle
        :param committee_id: The FEC id of a particular committee (required)
        :param cycle: (string) The cycle that you are intereested in the independant expenditures for, default is "2016"
        :return: All pages from the response from the api as JSOn
        """
        if committee_id is None:
            raise URIParameterException('Committee ID parameter required but not given')
        requeststr = str(self.uri) + 'committee/' + str(committee_id) + '/schedules/schedule_e/by_candidate/'
        params = {
            'api_key': self.apikey,
            'sort_hide_null': 'true',
            'per_page': '30',
            'cycle': str(cycle),
        }
        headers = {}
        return self.get_allpages(requeststr, params, headers)

    def get_committees(self):
        """
        Function to get all SuperPACs from the FEC
        :return: The api response containing all SuperPACs as json data
        """
        requeststr = str(self.uri) + 'committees/'
        params = {
            'api_key': self.apikey,
            'committee_type': 'O',
            'per_page': "100",
        }
        headers = {}
        return self.get_allpages(requeststr, params, headers)

    def get_allpages(self, requeststr, params, headers):
        """
        Helper functions to compile paginated responses into a single piece of json data
        :param requeststr: the request url string for the api
        :param params: the parameters for the request(anything in url after '?') as a dictionary
        :param headers: the headers for the request as a dictionary
        :return: all pages of the api result compiled into one
        """
        params['page'] = '1'
        data = super().request(requeststr, params, headers)
        results = data["results"]
        pages = data["pagination"]["pages"]

        for page in range(2, pages+1):
            params['page'] = str(page)
            results += super().request(requeststr, params, headers)["results"]
        return results
