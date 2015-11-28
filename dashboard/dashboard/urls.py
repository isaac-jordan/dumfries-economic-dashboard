from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^pages/home', 'dashboard.views.graphs', name='graphs'),
    url(r'^pages/about', 'dashboard.views.about', name='about'),
    url(r'^pages/savedConfigs', 'dashboard.views.savedConfigs', name='savedConfigs'),
    url(r'^pages/login', 'dashboard.views.loginPage', name='login'),
    url(r'^pages/register', 'dashboard.views.registrationPage', name='register'),
    url(r'^logout', 'dashboard.views.logoutUser', name='logout'),
    url(r'^account/login', 'dashboard.views.ajax_login', name='ajax_login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
