from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^photos/', include('photos.urls')),
    url(r'^rideshare/', include('rideshare.urls')),
    url(r'^rsvp/', include('rsvp.urls')),
    url(r'^updates/', include('updates.urls')),
)