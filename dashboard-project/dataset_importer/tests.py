"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Dataset
import json


class ImporterTest(TestCase):
    def setUp(self):
        Dataset.objects.get_or_create(name="test_dataset",
                                      dataJSON="""[{"x":"test"}]""")
        Dataset.objects.get_or_create(dataJSON="""[{"y":"test"}]""")
        
    def test_dataset_json(self):
        dataset = Dataset.objects.get(name="test_dataset")
        self.assertEqual(json.loads(dataset.dataJSON), [{"x":"test"}], "Dataset JSON did not load correctly.")
        
    def test_dataset_str(self):
        dataset = Dataset.objects.get(name="test_dataset")
        self.assertTrue(str(dataset) == dataset.name, "Dataset did not return correct name from __str__")
        dataset = Dataset.objects.get(pk=2)
        self.assertTrue(str(dataset) == "Imported Dataset " + str(dataset.pk), "Dataset without name did not return correct name from __str__")