from django.conf.urls.defaults import *
from wedding import views

urlpatterns = patterns('',
    url(r'^$', views.home, name="wedding_home"),
    url(r'^photos/', include('wedding.photos.urls')),
    url(r'^rideshare/', include('wedding.rideshare.urls')),
    url(r'^rsvp/', include('wedding.rsvp.urls')),
    url(r'^updates/', include('wedding.updates.urls')),
)