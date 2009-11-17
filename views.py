from django.shortcuts import render_to_response
from django.template import RequestContext

from wedding.updates.models import Update
from wedding.photos.models import Photo

def home(request):
    try:
        update = Update.objects.latest()
    except:
        update = None
    
    photos = Photo.objects.all()[:5]
    
    return render_to_response("home.html",
                             {'update': update, 'photos': photos},
                             context_instance=RequestContext(request))