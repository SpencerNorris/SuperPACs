import django
from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase
import os
srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


os.sys.path.append("/code/src/datasource")
print(os.sys.path)
from seeder import *
from api.models import *

from api.views import *
# Create your tests here.

#this file is for

##Class API to Pickle simple comparator.
##This testing class would test that all the data
## that is coming from the API's directly would get saved to pickles when required.
##and that the data for those pickles matches the same API data after it gets saved.

#What about API to pickle? or is that way too deep.
class CacheToORMTest(TestCase):
    ##creates a test_superpac database so we can fool around with testing.
    def setUp(self):
        self.api_seeder = APISeeder()

        print("(start)CacheToORMTest(setUp):--------")
        self.pickle_seeder = PickleSeeder()
        print("Using PickleSeeder seeder to get data.")
        self.pickle_seeder.seedAll(reset=False)
        print("Finished using PickleSeeder.")


        #print("Number of representatives:",len(Representative.objects.all()))
        print("Getting ORM values to compare with API json.")
        self.ted_cruz = Representative.objects.get(first_name="Ted",last_name="Cruz")
        self.elizabeth_warren = Representative.objects.get(first_name="Elizabeth",last_name="Warren")
        print("(end)CacheToORMTest(setUp):--------")

    ##clears the test_superpac database that was created in setUp()
    def tearDown(self):
        pass

    def test_partyperson(self):
        ##compare the data you can get from the Seeder to data in the original JSON
        ##essentially, create content based comparisons like this:
        ##self.api_seeder.getRepresentatives()["Ted_cruz"]["party"] == self.ted_cruz.party
        self.assertEqual(self.ted_cruz.party, 'R')
        self.assertEqual(self.elizabeth_warren.party, 'D')
        pass


#import django views to sanity check the front-end visualization contract.
class ViewsToFrontendTest(TestCase):
    def setUp(self):
        self.api_seeder = APISeeder()

        print("(start)ViewsToFrontendTest(setUp):--------")
        self.pickle_seeder = PickleSeeder()
        print("Using PickleSeeder seeder to get data.")
        self.pickle_seeder.seedAll(reset=False)


        print("Getting ORM values to compare with VIEW json.")
        self.ted_cruz = Representative.objects.get(first_name="Ted",last_name="Cruz")
        self.elizabeth_warren = Representative.objects.get(first_name="Elizabeth",last_name="Warren")
        print("(end)ViewsToFrontendTest(setUp):--------")

    def tearDown(self):
        pass

    def test_partyperson(self):
        ##compare the data you can get from the ORM to data in the view
        ##essentially, create content based comparisons like this:
        ##self.ted_cruz.party == views.donations()["ted_cruz"].party

        pass
