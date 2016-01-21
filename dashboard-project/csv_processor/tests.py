"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from csv_processor.models import CsvFile
import os, json

class ImportTest(TestCase):
    def test_file_does_not_exist(self):
        """Tests that an IOError is thrown if file doesn't exist."""
        csv = CsvFile.objects.get_or_create(filename="this_file_doesnt_exist.dud")[0]
        self.assertRaises(IOError, csv.importData)
        
    def test_import_all_result_not_empty(self):
        """Tests that csv can be read."""
        csv = CsvFile.objects.get_or_create(filename="test_employment.csv")[0]
        csvData = csv.importData()
        self.assertTrue(len(csvData) > 0, msg="CsvFile.importData() returned an empty sequence.")
        
    def test_importJson_is_exact(self):
        csv = CsvFile.objects.get_or_create(filename="test_employment.csv")[0]
        basepath = os.path.dirname(__file__)
        knownJson = open(os.path.abspath(os.path.join(basepath, "static", "csv_processor", "data", "test_employment.json"))).read()
        
        csvDataJson = csv.importJsonData()
        self.assertEqual(json.loads(knownJson), json.loads(csvDataJson), "Generated JSON doesn't match the known JSON.")