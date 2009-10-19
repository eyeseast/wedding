import datetime
import logging
import urllib

from django.conf import settings
from django.db import transaction
from django.utils.encoding import smart_unicode, force_unicode

from wedding.photos import utils
from wedding.photos.models import Photo

log = logging.getLogger('wedding.photos.utils.flickr')

# Using Jacobian's FlickClient from Jellyroll


class FlickrError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
    
    def __str__(self):
        return 'FlickrError %s: %s' % (self.code, self.message)


class FlickrClient(object):
    def __init__(self, api_key, method='flickr'):
        self.api_key = api_key
        self.method = method
        
    def __getattr__(self, method):
        return FlickrClient(self.api_key, '%s.%s' % (self.method, method))
        
    def __repr__(self):
        return "<FlickrClient: %s>" % self.method
        
    def __call__(self, **params):
        params['method'] = self.method
        params['api_key'] = self.api_key
        params['format'] = 'json'
        params['nojsoncallback'] = '1'
        url = "http://flickr.com/services/rest/?" + urllib.urlencode(params)
        json = utils.getjson(url)
        if json.get("stat", "") == "fail":
            raise FlickrError(json["code"], json["message"])
        return json


# Public API

def enabled():
    ok = (hasattr(settings, "FLICKR_API_KEY") and
          hasattr(settings, "FLICKR_GROUP_ID"))
    if not ok:
      log.warn('The Flickr provider is not available because the '
               'FLICKR_API_KEY and/or FLICKR_GROUP_ID settings '
               'are undefined.')
    return ok


def update():
    flickr = FlickrClient(settings.FLICKR_API_KEY)

    page = 1
    while True:
        log.debug("Fetching page %s of photos", page)
        resp = flickr.groups.pools.getPhotos(group_id=settings.FLICKR_GROUP_ID, extras="date_taken", per_page="500", page=str(page))
        photos = resp["photos"]
        if page > photos["pages"]:
            log.debug("Ran out of photos; stopping.")
            break
            
        for photodict in photos["photo"]:
            timestamp = utils.parsedate(str(photodict["datetaken"]))            
            photo_id = utils.safeint(photodict["id"])
            secret = smart_unicode(photodict["secret"])
            server = smart_unicode(photodict["server"])
            _handle_photo(flickr, photo_id, secret, license, timestamp)
            
        page += 1

# Private API

@transaction.commit_on_success
def _handle_photo(flickr, photo_id, secret, license, timestamp):
    info = flickr.photos.getInfo(photo_id=photo_id, secret=secret)["photo"]
    
    server_id = utils.safeint(info["server"])
    farm_id = utils.safeint(info["farm"])
    taken_by = smart_unicode(info["owner"]["username"])
    title = smart_unicode(info["title"]["_content"])
    description = smart_unicode(info["description"]["_content"])
    date_uploaded = datetime.datetime.fromtimestamp(utils.safeint(info["dates"]["posted"]))
    date_updated = datetime.datetime.fromtimestamp(utils.safeint(info["dates"]["lastupdate"]))
    
    log.debug("Handling photo: %r (taken %s)" % (title, timestamp))
    
    try:
        photo = Photo.objects.get(photo_id=photo_id)
    except Photo.DoesNotExist:
        photo = Photo(photo_id=photo_id)
    
    # at this point, we have a photo
    photo.farm_id = farm_id
    photo.server_id = server_id
    photo.secret = secret
    
    photo.title = title
    photo.description = description
    photo.taken_by = taken_by
    
    photo.date_uploaded = date_uploaded
    photo.date_updated = date_updated
    
    # save once, whether creating or updating
    photo.save()


