'''
File: datasource/__init__.py
Author: Spencer Norris
'''

import requests


class APIKeyException(Exception):
	'''
	Class for defining Datasource instantiation errors
	where the user has provided an API key or the name of the 
	API key parameter but not both.
	'''
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class Datasource:
	pass

class RESTDatasource(Datasource):
	def __init__(self, uri, apikey=None, keyname=None):

		#Throw API key errors
		if (apikey is None and not keyname is None):
			raise APIKeyException('API key parameter name provided but not the API key')
		elif (apikey is not None and keyname is None):
			raise APIKeyException('API key provided but not API key parameter name')

		super().__init__()
		self.uri = uri
		self.apikey = apikey
		self.keyname = keyname

	def request(self, method, **kwargs):
	'''
	Wrapper method for the Requests library.
	If apikey has been provided, expects the name of 
	the API key parameter for the URI under "kwargs['keyname']"
	'''
	if not self.apikey is None and not self.keyname is None:
		kwargs[kwargs['keyname']] = self.apikey
	r = requests.get(str(uri) + str(method), params=kwargs)
	return json.loads(r.text)
