from django.test import TestCase
from models import DashboardDatasource, Category, Visualisation, DashboardDataset, SavedConfig, SavedGraph

class TestDashboardModels(TestCase):
    def setUp(self):
        DashboardDatasource.objects.get_or_create(name="test_datasource")
        Category.objects.get_or_create(name="test_category")
        #Visualisation.objects.get_or_create(...)
        
    def test_datasource_str(self):
        ds = DashboardDatasource.objects.get(name="test_datasource")
        self.assertTrue(str(ds) == "test_datasource", "Datasource __str__ did not return correct value.")