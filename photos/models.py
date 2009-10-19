from django.db import models

# Create your models here.


class Photo(models.Model):
    "A photo on Flickr"
    
    # flickr metadata
    photo_id = models.CharField(max_length=50, unique=True, primary_key=True)
    farm_id = models.PositiveIntegerField(blank=True, null=True)
    server_id = models.PositiveIntegerField()
    secret = models.CharField(max_length=30, blank=True)
    
    # content metadata
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    taken_by = models.CharField(max_length=255, blank=True)
    
    # dates
    date_uploaded = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    
    
    class Meta:
        ordering = ('-date_uploaded',)
    
    
    def __unicode__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return self.url
    
    
    @property
    def farm(self):
        if self.farm_id:
            return ''.join(['farm', str(self.farm_id), '.'])
        return ''
    
    
    @property
    def url(self): # this is the photo page
        return u"http://www.flickr.com/photos/%s/%s/" % (self.taken_by, self.photo_id)
    
    
    def get_image_url(self, size=None):
        if size in list('mstbo'):
            return "http://%sstatic.flickr.com/%s/%s_%s_%s.jpg" % \
                (self.farm, self.server_id, self.photo_id, self.secret, size)
        else:
            return "http://%sstatic.flickr.com/%s/%s_%s.jpg" % \
                (self.farm, self.server_id, self.photo_id, self.secret)
    
    image_url = property(lambda self: self.get_image_url())
    square_url = property(lambda self: self.get_image_url('s'))
    thumbnail_url = property(lambda self: self.get_image_url('t'))
    small_url = property(lambda self: self.get_image_url('m'))
    large_url = property(lambda self: self.get_image_url('b'))
    original_url = property(lambda self: self.get_image_url('o'))

