"""
File: datasource\keytests.py
Author: Kevin Reitano
Description: The tests for confirming the validity of each data sources API Key
"""
import requests


def test_FEC_key(apikey=None):
    """

    :param apikey:
    :return:
    """
    if apikey is None:
        print('No FEC API Key provided')
        return False
    uri = "https://api.open.fec.gov/v1/committee/C00607275/schedules/schedule_e/by_candidate/"
    params = {
        'api_key': apikey,
        'sort_hide_null': 'true',
        'per_page': '30',
        'cycle': '2016',
    }
    result = requests.get(uri, params=params)
    if result.status_code == '200':
        return True
    else:
        print('Unexpected status_code when testing FEC API Key:')
        print(result.status_code)
        return False


def test_OS_key(apikey=None):
    """

    :param apikey:
    :return:
    """
    if apikey is None:
        print('No OpenSecrets API Key provided')
        return False
    uri = "https://www.opensecrets.org/api/"
    params = {
        'api_key': apikey,
        'id': 'RI',
        'output': 'json',
    }
    result = requests.get(uri, params=params)
    if result.status_code == '200':
        return True
    else:
        print('Unexpected status code when testing FEC API Key:')
        print(result.status_code)
        return False



def test_PP_key(apikey=None):
    if apikey is None:
        print('No OpenSecrets API Key provided')
        return False
    uri = "https://api.propublica.org/campaign-finance/v1/2016/committees/search"
    params = {
        'query': 'gol',
    }
    headers = {'X-API-Key': apikey}
    result = requests.get(uri, params=params, headers=headers)
    if result.status_code == '200':
        return True
    else:
        print('Unexpected status code when testing FEC API Key:')
        print(result.status_code)
        return False
