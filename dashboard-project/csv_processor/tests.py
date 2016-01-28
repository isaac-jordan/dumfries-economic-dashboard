# coding=UTF8
"""
Test classes for CsvFile model.
"""

from django.test import TestCase
from django.core.files import File
from csv_processor.models import CsvFile, Dimension
from dashboard.models import Category, Datasource, Visualisation, DashboardDataset
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
        
    def test_csv_import_data_not_none(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        data = csvFile.importData()
        self.assertIsNotNone(data, "Result from CsvFile.importData is null.")
        
    def test_csv_import_data_returns_one_dataset(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        data = csvFile.importData()
        self.assertTrue(len(data) == 1, "CsvFile.importData returned incorrect number of datasets for 2 Dimensions")
        
    def test_csv_import_data_returns_two_datasets(self):
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
        
    def test_csv_import_json_data_returns_string(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        jsonData = csvFile.importJsonData()
        self.assertTrue(type(jsonData) is str, "CsvFile.importJsonData did not return a string")
        self.assertTrue(len(json.loads(jsonData)) == 1, "CsvFile.importJsonData returned incorrect number of datasets for 2 Dimensions")
        
    def test_csv_import_create_dashboard_info_works(self):
        csvFile = CsvFile.objects.get(visualisationName="test_real_monthly_test")
        csvFile.createDashboardInfo()
        vis = Visualisation.objects.get(name=csvFile.visualisationName)
        datasets = DashboardDataset.objects.filter(visualisation=vis)
        self.assertTrue(len(datasets) == 1, "CsvFile.createDashboardInfo created incorrect number of datasets for 2 Dimensions")
        self.assertTrue(len(json.loads(csvFile.dataJson)) == 1, "CsvFile.createDashboardInfo made dataJson incorrect for 2 Dimensions")