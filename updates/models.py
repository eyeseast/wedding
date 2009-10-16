import datetime

from django.contrib.auth.models import User
from django.db import models

class UpdateManager(models.Manager):
    def live(self):
        return self.filter(public=True)


class Update(models.Model):
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    public = models.BooleanField(default=True)
    
    objects = UpdateManager()
    
    
    class Meta:
        get_latest_by = "pub_date"
        ordering = ('-pub_date',)
    
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.text[:50]


    @models.permalink
    def get_absolute_url(self):
        return ("updates_update_detail", None, {'object_id': self.id})