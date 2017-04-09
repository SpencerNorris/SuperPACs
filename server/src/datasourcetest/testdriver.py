"""
File: datasource\testdriver.py
Author: Kevin Reitano
Description: The main driver for datasource unit tests
"""

import os
srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

restpath = srcpath
os.sys.path.append(restpath)

from methodtests import *

FEC_APIKEY = os.getenv('FEC_API_KEY', '')
ProPublica_APIKEY = os.getenv('PP_API_KEY', '')
OpenSecrets_APIKEY = os.getenv('OS_API_KEY', '')


def run_method_tests(passCnt = 0, totalCnt = 0):
    """

    :param passCnt:
    :param totalCnt:
    :return:
    """
    passCnt, totalCnt = test_fec_methods(passCnt, totalCnt)
    passCnt, totalCnt = test_pp_methods(passCnt, totalCnt)
    passCnt, totalCnt = test_os_methods(passCnt, totalCnt)

    return passCnt, totalCnt


def test_fec_methods(passCnt=0, totalCnt = 0):
    """
    Calls tests for FEC API methods
    :param passCnt: Number of passed tests
    :param totalCnt: Total number of tests
    :return: Updated values for passed and total tests
    """
    if(methodtests.testfec_get_committees(FEC_APIKEY)):
        passCnt += 1
    totalCnt+=1

    return passCnt, totalCnt


def test_pp_methods(passCnt=0, totalCnt=0):
    """
    Calls tests for ProPublica API methods
    :param passCnt: Number of passed tests
    :param totalCnt: Total number of tests
    :return: Updated values for passed and total tests
    """
    if (methodtests.testpp_list_members(ProPublica_APIKEY)):
        passCnt += 1
    totalCnt += 1
    if (methodtests.testpp_get_indep_expends(ProPublica_APIKEY)):
        passCnt += 1
    totalCnt += 1


    return passCnt, totalCnt


def test_os_methods(passCnt=0, totalCnt=0):
    """
    Calls tests for ProPublica API methods
    :param passCnt: Number of passed tests
    :param totalCnt: Total number of tests
    :return: Updated values for passed and total tests
    """

    return passCnt, totalCnt



if __name__ == '__main__':
    print('Running API Method Tests')
    passCnt, totalCnt = run_method_tests(0, 0)
    print("passed " + str(passCnt) + " of " + str(totalCnt) + " tests")