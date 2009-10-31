"""
When people RSVP for a wedding, what do we need to know?

First, we need to know if they're coming.

Who are they? How many people are coming, and who are they?
What do they want to eat? (This assumes there are options)

We might also want to know where they're coming from,
so they can coordinate rides.

From us, they need to know how to get to the wedding,
what to wear and where we're registered.

We also want to tell them about the Flickr group, so
they can upload their photos to our online wedding album.

We also make one other assumption here: People RSVP in groups.
A family of six (i.e. mine) won't RSVP six times. One person
will respond with six names.
"""

from django.contrib.auth.models import User
from django.db import models


class RSVP(models.Model):
    RESPONSE_CHOICES = (
        ('yes', "Yes, we'll be there."),
        ('no', "Sorry, can't make it.")
    )
    group_name = models.CharField(max_length=255)
    response = models.CharField(max_length=5, choices=RESPONSE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        get_latest_by = "date"
        ordering = ('-date',)
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"
    
    
    def __unicode__(self):
        return self.group_name


class Guest(models.Model):
    group = models.ForeignKey(RSVP)
    user = models.ForeignKey(User, unique=True)
    
    # denormalized fields for simpler admin editing
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)