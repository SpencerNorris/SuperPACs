'''
File: datasource/__init__.py
Author: Spencer Norris
'''

import requests


class Datasource:
	pass

class RESTDatasource(Datasource):
	def __init__(self, uri):
		super().__init__()
		self.uri = uri

	def request(self, method, **kwargs):
	'''
	Wrapper method for the Requests library.
	'''
	r = requests.get(str(uri) + str(method), params=kwargs)
	return json.loads(r.text)
