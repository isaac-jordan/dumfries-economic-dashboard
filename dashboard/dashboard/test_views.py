import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from django.core.urlresolvers import reverse

from models import Datasource, Dataset, Visualisation, SavedConfig, SavedGraph

class TestAuthViews(TestCase):
    def setUp(self):
        User.objects.create_user("user@example.com", password="test1234")

    def test_login_view_loads_anonymous(self):
        """Check login page loads when user is anonymous."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.djhtml')
        
    def test_login_view_loads_logged_in(self):
        """Check login page loads when user is logged in."""
        self.client.login(username='user@example.com', password='test1234')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.djhtml')

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
        vis1 = Visualisation.objects.create(dataSource=ds1, name="TestVis", sizeX=2, sizeY=2, yLabel="Y-Label", xLabel="X-Label")
        Dataset.objects.create(visualisation=vis1, dataJSON=json.dumps([{"x":5,"y":10},{"x":7,"y":15}]))
        
    def test_ajax_getGraphs_view_loads(self):
        """Check AJAX getGraphs returns all graphs"""
        response = self.client.get(reverse('ajax_getGraphs'))
        jsonResponse = json.loads(response.content)
        self.assertTrue(len(jsonResponse['widgets']) > 0, "Widget list should be not empty.")
        
        