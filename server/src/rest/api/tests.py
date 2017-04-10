import django
from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase
import os
srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


os.sys.path.append("/code/src/datasource")
print(os.sys.path)
from seeder import *
from api.models import Representative
# Create your tests here.





class CongressTest(TestCase):
    def setUp(self):
        uploadToDatabase('/code/src/datasource/donationdata.pickle')
        print("number of representatives:",len(Representative.objects.all()))
        self.ted_cruz = Representative.objects.get(first_name="Ted",last_name="Cruz")
        self.elizabeth_warren = Representative.objects.get(first_name="Elizabeth",last_name="Warren")


    def tearDown(self):
        pass

    def test_partyperson(self):
        self.assertEqual(self.ted_cruz.party, 'R')
        self.assertEqual(self.elizabeth_warren.party, 'D')
        pass
