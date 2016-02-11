from django.test import TestCase
from models import DashboardDatasource, Category, Visualisation, DashboardDataset, SavedConfig, SavedGraph
import json

class TestDashboardModels(TestCase):
    def setUp(self):
        DashboardDatasource.objects.get_or_create(name="test_datasource")
        Category.objects.get_or_create(name="test_category")
        #Visualisation.objects.get_or_create(...)
        
    def test_datasource_str(self):
        ds = DashboardDatasource.objects.get(name="test_datasource")
        self.assertTrue(str(ds) == "test_datasource", "Datasource __str__ did not return correct value.")

class TestVisualisation(TestCase):
    def setUp(self):
        dataset={
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }
        cat =Category.objects.get_or_create(name="test_category")
        ds =DashboardDatasource.objects.get_or_create(name="test_datasource")
        vis = Visualisation.objects.get_or_create(dataSource=ds,name="testVis",category=cat,type="line",xLabel="Year",sizeY=2,sizeX=2)
        data = DashboardDataset.object.get_or_create(name='testDataSet',dataJSON=json.dumps(dataset),visualisation=vis)
    def testGetWidget(self):
        dataset={
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }
        testWidget={
            'name': "testVis",
                           'id': "vis1",
                           'pk': 1,
                           'category': "test_category",
                           'type': "line",
                           'dataset': dataset,
                           'sourceName': "test_datasource",
                           'sourceLink': None,
                           'sizeX': 2,
                           'sizeY': 2
        }
        testVis= Visualisation.objects.get(name="testVis")
        testVisDict=testVis.getWidget()
        argument = True
        for k in testWidget:
            if(type(testWidget[k]) is dict):
                for k1 in testWidget[k]:
                    if(k1!=testVisDict[k][k1]):
                        print "The widgets are not the same"
                        argument = False
                        break
            else:
                if(testWidget[k] != testVisDict[k]):
                    print "the widgets are not the same"
                    argument = False
                    break
        self.assertTrue(argument,"the two widgets are not the same")


