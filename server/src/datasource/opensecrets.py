'''
File: datasource/propublica.py
Author: Kevin Reitano
Description: Implementation of clients for
the OpenSecrets Api.
'''

from datasource import RESTDatasource
from datasource import APIKeyException
from datasource import URIParameterException


class OpenSecretsAPI(RESTDatasource):
    def __init__(self, apikey=None):
        """
        Constructor for the OpenSecretsAPI class
        :param apikey: The OpenSecretsAPI key
        """
        if apikey is None:
            raise APIKeyException('API key not provided')
        super().__init__(apikey)
        self.uri = "https://www.opensecrets.org/api/"

    def get_legislators(self, subset=None):
        """
        API Method for calling the getLegislators method in the OpenSecrets API.
        Can get attributes for a specified subset(state, district, or specific CID)
        :param subset: either a 2 letter state code or a 4 char district or specific CID
        :return: The response for the getLegislators method as json
        """
        rheaders = {}
        rparams = {"apikey": self.apikey}
        if subset is None:
            raise URIParameterException('Subset ID required but not provided')
        else:
            rparams['id'] = str(subset)
        rparams['output'] = 'json'
        requeststr = str(self.uri)
        return super().request(requeststr, rparams, rheaders)

