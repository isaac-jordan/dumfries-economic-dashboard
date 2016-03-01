import json, datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from csv_processor import util
from dataset_importer import util as dateutil
from dateutil.tz import *


from models import Datasource, DashboardDataset, Visualisation, SavedConfig, SavedGraph, Category

class TestAuthViews(TestCase):
    def setUp(self):
        User.objects.create_user("user@example.com", password="test1234")

    def test_login_view_loads_anonymous(self):
        """Check login page loads when user is anonymous."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/login.djhtml')
        
    def test_login_view_loads_logged_in(self):
        """Check login page loads when user is logged in."""
        self.client.login(username='user@example.com', password='test1234')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/login.djhtml')
        response = self.client.get(reverse('savedConfigs'))
        self.assertTemplateUsed(response, 'dashboard/pages/savedConfigs.djhtml')
        print response.context['configurations']
        self.assertTrue(not response.context['configurations'])

    def test_ajax_login_view_fails_blank(self):
        """Check AJAX login handles blank data dictionary."""
        response = self.client.post(reverse('ajax_login'), {})
        self.assertEqual(json.loads(response.content)['success'], False)

    def test_ajax_login_view_fails_invalid(self):
        """Check AJAX login handles invalid login details."""
        response = self.client.post(reverse('ajax_login'), {"email":"tester@wrong.com", "password":"wrongPass"})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'], False)

    def test_ajax_login_view_pass_valid(self):
        """Check AJAX login works with correct details."""
        response = self.client.post(reverse('ajax_login'), {"email":"user@example.com", "password":"test1234"})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'], True)
        self.assertTrue(SESSION_KEY in self.client.session)
        
    def test_logout_view_pass_valid(self):
        """Check logout works when user is logged in."""
        self.client.login(username='user@example.com', password='test1234')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(SESSION_KEY not in self.client.session)

    def test_ajax_register(self):
        response = self.client.post(reverse('ajax_register'),{'email':"test@test.com", "password":"test"})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'],True)

    def test_ajax_register_existing_user(self):
        response = self.client.post(reverse('ajax_register'),{'email':"user@example.com", "password":"test1234"})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'],False)

    def test_ajax_register_emptyEmail(self):
        response = self.client.post(reverse('ajax_register'),{'email':"", "password":"test"})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'],False)

    def test_ajax_register_emptyPassword(self):
        response = self.client.post(reverse('ajax_register'),{'email':"test@test.com", "password":""})
        jsonResponse = json.loads(response.content)
        self.assertEqual(jsonResponse['success'],False)

    def test_registrationPage(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/register.djhtml')

    def test_ajax_isAuthenticated(self):
        self.client.login(username='user@example.com', password='test1234')
        response = self.client.get(reverse('ajax_checkAuthenticated'))
        r = json.loads(response.content)
        self.assertEqual(r['is_authenticated'], True)
        
class TestSavedConfigView(TestCase):
    def setUp(self):
        User.objects.create_user("user", "test@example.com", "test")
    
    def test_savedConfig_view_denies_anonymous(self):
        """Check that savedConfigs denies anonymous users and redirects to login page."""
        response = self.client.get(reverse('savedConfigs'), follow=True)
        self.assertRedirects(response, reverse('login') + "/?next=" + reverse('savedConfigs'))
        response = self.client.post(reverse('ajax_login'), follow=True)
        self.assertEqual(json.loads(response.content)['success'], False)
        
class TestGraphsView(TestCase):
    def setUp(self):
        ds1 = Datasource.objects.create(name="test")
        cat = Category.objects.create(name="CategoryTest")
        vis1 = Visualisation.objects.create(dataSource=ds1, category=cat, name="TestVis", sizeX=2, sizeY=2, yLabel="Y-Label", xLabel="X-Label")
        DashboardDataset.objects.create(visualisation=vis1, dataJSON=json.dumps([{"x":5,"y":10},{"x":7,"y":15}]))

    def test_ajax_getGraph(self):
        vis1 = Visualisation.objects.get(name = 'TestVis')
        response = self.client.get(reverse('ajax_getGraph'), {"id": vis1.pk})
        jsonResponse=json.loads(response.content)
        self.assertEqual(jsonResponse["pk"],vis1.pk)

    def test_ajax_getGraph_noID(self):
        vis1 = Visualisation.objects.get(name='TestVis')
        response = self.client.get(reverse('ajax_getGraph'))
        self.assertEqual(response.status_code, 400)

    def test_graphs_view_loads(self):
        response = self.client.get(reverse('graphs'))
        self.assertTrue(response, "Graph view returned a falsy object.")
        
    def test_ajax_getGraphs_view_loads(self):
        """Check AJAX getGraphs returns all graphs"""
        response = self.client.get(reverse('ajax_getGraphs'))
        jsonResponse = json.loads(response.content)
        self.assertTrue(len(jsonResponse['widgets']) > 0, "Widget list should be not empty.")
        
class TestSearchView(TestCase):
    def setUp(self):
        ds1 = Datasource.objects.create(name="test")
        ds2 = Datasource.objects.create(name="STUFF")
        cat = Category.objects.create(name="CategoryTest")
        cat2 = Category.objects.create(name="STUFF")
        vis1 = Visualisation.objects.create(dataSource=ds1, category=cat, name="TestVis", sizeX=2, sizeY=2, yLabel="Y-Label", xLabel="X-Label")
        DashboardDataset.objects.create(visualisation=vis1, dataJSON=json.dumps([{"x":20,"y":152},{"x":20,"y":185}]))
        vis2 = Visualisation.objects.create(dataSource=ds2, category=cat2, name="STUFF", sizeX=2, sizeY=2, yLabel="Y-Label", xLabel="X-Label")
        DashboardDataset.objects.create(visualisation=vis2, dataJSON=json.dumps([{"x":datetime.datetime(2000,1,1),"y":152},{"x":datetime.datetime(2002,1,1),"y":185}],cls=dateutil.DatetimeEncoder))

    def test_search_returns_result(self):
        response = self.client.get(reverse('search', kwargs={"searchTerm": "test" }))
        self.assertTrue(len(response.context["results"]) == 1, "Search test returned incorrect number of results.")
        self.assertTrue(response.context["results"][0]["name"] == "TestVis", "Search result has incorrect name")
        self.assertTemplateUsed(response,'dashboard/pages/searchResults.djhtml')

    def test_searchTerm_is_None(self):
        response = self.client.get(reverse('search',kwargs={"searchTerm":'' }))
        self.assertTemplateUsed(response, 'dashboard/pages/searchResults.djhtml')

    def test_category_list(self):
        testcategories = Category.objects.all()
        response = self.client.get(reverse('categoryList'))
        testing = response.context['categories']
        self.assertTemplateUsed(response, 'dashboard/pages/categoryList.djhtml')
        for f,b in zip(testing,testcategories):
            self.assertEqual(f,b)

    def test_category_view(self):
         response = self.client.get(reverse('category', kwargs={"categoryName" : "STUFF" }))
         self.assertTemplateUsed(response, 'dashboard/pages/category.djhtml')
         self.assertTrue(response.context['error'] is None)
         testList = [{'sourceName': u'STUFF', 'sizeX': 2, 'sizeY': 2, 'dataset': [[{u'y': 152, u'x': u'2000-01-01T00:00:00Z'}, {u'y': 185, u'x': u'2002-01-01T00:00:00Z'}]], 'trends': {'minY': {'y': 152, 'x': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=tzutc())}, 'maxY': {'y': 185, 'x': datetime.datetime(2002, 1, 1, 0, 0, tzinfo=tzutc())}, 'analysis': [{'name': 'Dashboard Dataset 2'}]}, 'xLabel': u'X-Label', 'yLabel': u'Y-Label', 'id': 'vis2', 'category': u'STUFF', 'name': u'STUFF', 'sourceLink': u'', 'datasetLabels': [None], 'pk': 2, 'type': u''}]
         self.assertTrue(response.context['category'].name == "STUFF")
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
         testDict = deep_sort(testList[0])
         testDict2=deep_sort(response.context['widgets'][0])
         self.assertDictEqual(testDict, testDict2, "getWidget() did not return the correct widget.")

    def test_category_view_less_than_one_category(self):
        response = self.client.get(reverse('category', kwargs={"categoryName" : "NONETest" }))
        self.assertTrue(response.context['error']=="Category 'NONETest' name not found.")

    def test_ajax_GetTrend(self):
        vis1 = Visualisation.objects.get(name='STUFF')
        response = self.client.get(reverse('ajax_getTrend'),{"id": vis1.pk})
        jsonResponse=json.loads(response.content)
        self.assertEqual(jsonResponse["pk"],vis1.pk)

    def test_ajax_getTrend_noID(self):
        vis1 = Visualisation.objects.get(name='STUFF')
        response = self.client.get(reverse('ajax_getTrend'))
        self.assertEqual(response.status_code, 400)









        
        