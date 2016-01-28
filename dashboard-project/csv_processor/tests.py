# coding=UTF8
"""
Test classes for CsvFile model.
"""

from django.test import TestCase
from django.core.files import File
from csv_processor.models import CsvFile, Dimension
from dashboard.models import Category, Datasource
import os, json

class CSVImportTest(TestCase):
    def setUp(self):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "static", "csv_processor", "test", "data", "test_real_monthly.csv"))
        f = File(open(filepath))
        category = Category.objects.get_or_create(name="test_category")[0]
        dataSource = Datasource.objects.get_or_create(name="test_datasource")[0]
        csvFile = CsvFile.objects.get_or_create(visualisationName="test_real_monthly_test",
                                      category = category,
                                      dataSource = dataSource,
                                      upload = f,
                                      source = "http://test.example.com"
                                      )[0]
        Dimension.objects.get_or_create(label="Dumfries and Galloway",
                                        indexForLabel = 1,
                                        type = Dimension.TYPE_CHOICES[0][0],
                                        dataStartIndex = 2,
                                        dataEndIndex = 151,
                                        dataType = Dimension.DATA_CHOICES[1][0],
                                        dataFormat = "£",
                                        makeXaxisOnGraph = False,
                                        csvFile = csvFile)
        Dimension.objects.get_or_create(label="Month-Year",
                                        index = 5,
                                        type = Dimension.TYPE_CHOICES[0][0],
                                        dataStartIndex = 2,
                                        dataEndIndex = 151,
                                        dataType = Dimension.DATA_CHOICES[0][0],
                                        dataFormat = "%b-%y",
                                        makeXaxisOnGraph = True,
                                        csvFile = csvFile)
        
    def test_import_data_not_none(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        data = csvFile.importData()
        self.assertIsNotNone(data, "Result from CsvFile.importData is null.")
        
    def test_import_data_returns_one_dataset(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        data = csvFile.importData()
        self.assertTrue(len(data) == 1, "CsvFile.importData returned incorrect number of datasets for 2 Dimensions")
        
    def test_import_data_returns_two_datasets(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        Dimension.objects.get_or_create(label="Scotland",
                                        indexForLabel = 1,
                                        type = Dimension.TYPE_CHOICES[0][0],
                                        dataStartIndex = 2,
                                        dataEndIndex = 151,
                                        dataType = Dimension.DATA_CHOICES[1][0],
                                        dataFormat = "£",
                                        makeXaxisOnGraph = False,
                                        csvFile = csvFile)
        data = csvFile.importData()
        self.assertTrue(len(data) == 2, "CsvFile.importData returned incorrect number of datasets for 3 Dimensions")