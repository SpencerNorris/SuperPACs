'''
File: datasource/propublica.py
Author: Spencer Norris
Description: Implementation of clients for
the Propublica Campaign Finance and Congress APIs.
'''

from datasource import RESTDatasource

class CampaignFinanceAPI(RESTDatasource):
	def __init__(self, uri):
		super().__init__(uri)


class CongressAPI(RESTDatasource):
	def __init__(self, uri):
		super().__init__(uri)