from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^pages/home', 'dashboard.views.graphs', name='graphs'),
    url(r'^pages/category/(?P<categoryName>.*)', 'dashboard.views.category', name='category'),
    url(r'^pages/category$', 'dashboard.views.categoryList', name='categoryList'),
    url(r'^pages/savedConfigs', 'dashboard.views.savedConfigs', name='savedConfigs'),
    url(r'^pages/login', 'dashboard.views.loginPage', name='login'),
    url(r'^pages/register', 'dashboard.views.registrationPage', name='register'),
    url(r'^saveConfig', 'dashboard.views.saveConfig', name='saveConfig'),
    url(r'^deleteSavedConfig', 'dashboard.views.ajaxDeleteSavedConfig', name='ajax_deleteSavedConfig'),
    url(r'^loadSavedConfig', 'dashboard.views.ajaxloadSavedConfig', name='ajax_loadSavedConfig'),
    url(r'^getGraphs', 'dashboard.views.ajaxGetGraphs', name='ajax_getGraphs'),
    url(r'^logout', 'dashboard.views.logoutUser', name='logout'),
    url(r'^account/checkAuthenticated', 'dashboard.views.ajax_isAuthenticated', name='ajax_checkAuthenticated'),
    url(r'^account/login', 'dashboard.views.ajax_login', name='ajax_login'),
    url(r'^account/register', 'dashboard.views.ajax_register', name='ajax_register'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'test_trends', 'dashboard.views.trends'),
)
