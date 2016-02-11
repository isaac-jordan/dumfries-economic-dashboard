from django.test import TestCase
from django.contrib.auth.models import User
from models import DashboardDatasource, Category, Visualisation, DashboardDataset, SavedConfig, SavedGraph
import json

def setUpEntries():
    ds = DashboardDatasource.objects.get_or_create(name="test_datasource")[0]
    dataset=[{
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
            }]
    JSONdataset=json.dumps(dataset)
    cat = Category.objects.get_or_create(name="test_category")[0]
    vis = Visualisation.objects.get_or_create(dataSource=ds, name="testVis", category=cat, type="line", xLabel="Year", sizeY=2, sizeX=2)[0]
    data = DashboardDataset.objects.get_or_create(name='testDataSet', dataJSON=JSONdataset, visualisation=vis)[0]
    
    user = User.objects.create_user(username='test', email='test@...', password='top_secret')
    savedconfig = SavedConfig.objects.get_or_create(name="testSavedConfig", user=user)[0]
    savedgraph = SavedGraph.objects.get_or_create(visualisation=vis, savedConfig=savedconfig, xPosition=5, yPosition=2, sizeX=2, sizeY=2)
        
class TestDashboardDatasource(TestCase):
    def setUp(self):
        setUpEntries()
        
    def test_datasource_str(self):
        ds = DashboardDatasource.objects.get(name="test_datasource")
        self.assertTrue(str(ds) == "test_datasource", "Datasource __str__ did not return correct string.")
        
    def test_get_all_widgets_correct_number(self):
        ds = DashboardDatasource.objects.get(name="test_datasource")
        widgets = ds.getAllWidgets()
        
        self.assertTrue(len(widgets) == 1, "GetAllWidgets returned incorrect number of widgets")
        
class TestCategory(TestCase):
    def setUp(self):
        setUpEntries()
        
    def test_category_str(self):
        cat = Category.objects.get(name="test_category")
        self.assertTrue(str(cat) == "test_category", "Category __str__ did not return correct string.")

class TestDashboardDataset(TestCase):
    def setUp(self):
        setUpEntries()
        vis = Visualisation.objects.get(name="testVis")
        DashboardDataset.objects.get_or_create(dataJSON="[]", visualisation=vis)
    
    def test_visualisation_str(self):
        data = DashboardDataset.objects.get(name="testDataSet")
        anon = DashboardDataset.objects.get(pk = 2)
        self.assertTrue(str(data) == "testDataSet", "DashboardDataset __str__ with name did not return correct string.")
        self.assertTrue(str(anon) == "Dashboard Dataset 2", "DashboardDataset __str__ without name did not return correct string.")

class TestSavedConfig(TestCase):
    def setUp(self):
        setUpEntries()
        
    def test_savedconfig_str(self):
        config = SavedConfig.objects.get(name="testSavedConfig")
        self.assertTrue(str(config) == "testSavedConfig", "SavedConfig __str__ did not return correct string.")

class TestSavedGraph(TestCase):
    def setUp(self):
        setUpEntries()
        
    def test_savedconfig_str(self):
        config = SavedConfig.objects.get(name="testSavedConfig")
        graph = SavedGraph.objects.get(savedConfig=config)
        self.assertTrue(str(graph) == "Saved Graph 1", "SavedGraph __str__ did not return correct string.")

class TestVisualisation(TestCase):
    def setUp(self):
        setUpEntries()
        
    def test_getWidget_returns_correct(self):
        def deep_sort(obj):
            """
            Recursively sort list or dict nested lists
            """
        
            if isinstance(obj, dict):
                _sorted = {}
                for key in sorted(obj):
                    _sorted[key] = deep_sort(obj[key])
        
            elif isinstance(obj, list):
                new_list = []
                for val in obj:
                    new_list.append(deep_sort(val))
                _sorted = sorted(new_list)
        
            else:
                _sorted = obj
        
            return _sorted
    
        dataset=[{
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
            }]
        JSONdataset=json.dumps(dataset)
        testWidget={
            'name': "testVis",
                           'id': "vis1",
                           'pk': 1,
                           'category': "test_category",
                           'type': "line",
                           'dataset': [json.loads(JSONdataset)],
                           'sourceName': "test_datasource",
                           'sourceLink': '',
                           'sizeX': 2,
                           'sizeY': 2
        }
        testVis= Visualisation.objects.get(name="testVis")
        testVisDict=testVis.getWidget()

        testVisDict = deep_sort(testVisDict)
        testWidget = deep_sort(testWidget)
    
        self.assertDictEqual(testWidget, testVisDict, "getWidget() did not return the correct widget.")
        
    def test_visualisation_str(self):
        vis = Visualisation.objects.get(name="testVis")
        self.assertTrue(str(vis) == "testVis", "Visualisation __str__ did not return correct string.")
        
    def test_calculateTrendData_minmax_correct(self):
        vis = Visualisation.objects.get(name="testVis")
        trendData = vis.calculateTrendData()
        self.assertTrue(trendData["maxY"] == {"y": 199,"x": 2006}, "CalculateTrendData returned wrong maxY item.")
        self.assertTrue(trendData["minY"] == {"y": 134,"x": 2008}, "CalculateTrendData returned wrong minY item.")


