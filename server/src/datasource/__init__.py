"""
File: datasource/__init__.py
Author: Spencer Norris and Kevin Reitano
Description: Implementation of Datasource base class.
"""

import requests
import json


class APIKeyException(Exception):
    """
    Class for defining Datasource instantiation errors
    where the user has provided an API key or the name of the
    API key parameter but not both.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class URIParameterException(Exception):
    """
    Class for defining Datasource method call errors
    where the user has failed to provide a required parameter
    for a given api method
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class RESTDatasource:
    def __init__(self, apikey=None):

        #Throw API key errors
        if (apikey is None):
            raise APIKeyException('API key not provided')
        super().__init__()
        self.apikey = apikey
        

    def request(self, requeststr, params, headers):
        """
        Wrapper method for the Requests library.
        Requires the uri of the request as well as parameters
        and headers, which vary by method although an api key
        will be required in some form.
        """
        r = requests.get(str(requeststr), params=params, headers=headers)
        return json.loads(r.text)
