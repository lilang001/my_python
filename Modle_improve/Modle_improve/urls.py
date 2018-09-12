from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'home_view.views.home', name='home'),
    url(r'^tuple', 'home_view.views.tuple', name='tuple'),
    url(r'^list', 'home_view.views.list', name='list'),
    url(r'^count/(\d+)', 'home_view.views.count', name='count'),
    url(r'^script', 'home_view.views.script', name='script'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
