"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from csv_processor.models import CsvFile

class SimpleTest(TestCase):
    def test_import_result_not_empty(self):
        """Tests that csv can be read."""
        csv = CsvFile.objects.get_or_create(filename="employment.csv")[0]
        csvData = csv.importData()
        self.assertTrue(len(csvData) > 0, msg="CsvFile.importData() returned an empty sequence.")