from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^photos/', include('wedding.photos.urls')),
    url(r'^rideshare/', include('wedding.rideshare.urls')),
    url(r'^rsvp/', include('wedding.rsvp.urls')),
    url(r'^updates/', include('wedding.updates.urls')),
)