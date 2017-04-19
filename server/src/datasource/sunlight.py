from datasource import RESTDatasource

class SunlightAPI(RESTDatasource):
	def __init__(self):
		apikey = '' #Sunlight doesn't require one!
		super().__init__(apikey)


	def search(self, query="obamacare"):
		'''
		From the Sunlight API documentation:

		Search the full text of legislation, and other fields.
		The query parameter allows wildcards, quoting for phrases, and nearby
		word operators (full reference) You can also retrieve highlighted excerpts,
		and all normal operators and filters.
		This searches the bill’s full text, short_title, official_title, popular_title, 
		nicknames, summary, and keywords fields.

		For a list of fields which can be used for filtering, see:
		https://sunlightlabs.github.io/congress/bills.html .

		Append the desired fields as keys in **params, such as:
		{
			'enacted_as.law_type' : 'private'
		}
		'''
		endpoint = 'https://congress.api.sunlightfoundation.com/bills/search'
		params = {}
		params['query'] = query
		return super().request(endpoint, params, {})


	def bills(self, bill_id):
		'''
		The main endpoint of Sunlight for retrieving data about legislation.
		Various parameters can be passed to retrieve bills according to certain criteria.

		For a list of fields which can be used for filtering, see:
		https://sunlightlabs.github.io/congress/bills.html .

			Append the desired fields as keys in **params, such as:
		{
			'enacted_as.law_type' : 'private'
		}
		'''
		params = {}
		params['bill_id'] = bill_id
		endpoint = 'https://congress.api.sunlightfoundation.com/bills'
		return super().request(endpoint, params, {})


	def votes(self, bill_id):
		'''
		The main endpoint of Sunlight for retrieving data about votes.
		Various parameters can be passed to retrieve votes according to certain criteria.

		For a list of fields which can be used for filtering, see:
		https://sunlightlabs.github.io/congress/bills.html .

			Append the desired fields as keys in **params, such as:
		{
			'enacted_as.law_type' : 'private'
		}

		Most relevant to us is how to retrieve votes related to a particular bill.
		In order to do this, append the bill_id to **params. For example:
		{
			"bill_id": "hr41-113"
		}

		The following is an example return value:
		{
		  "roll_id": "h7-2013",
		  "chamber": "house",
		  "number": 7,
		  "year": 2013,
		  "congress": 113,
		  "voted_at": "2013-01-04T16:22:00Z",
		  "vote_type": "passage",
		  "roll_type": "On Motion to Suspend the Rules and Pass",
		  "question": "On Motion to Suspend the Rules and Pass -- H.R. 41 -- To temporarily increase the borrowing authority of the Federal Emergency Management Agency for carrying out the National Flood Insurance Program",
		  "required": "2/3",
		  "result": "Passed",
		  "source": "http://clerk.house.gov/evs/2013/roll007.xml"
		}
		'''
		endpoint = 'https://congress.api.sunlightfoundation.com/votes'
		params = {}
		params['bill_id'] = bill_id
		return super().request(endpoint, params, {})
