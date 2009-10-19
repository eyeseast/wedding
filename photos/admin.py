from django.contrib import admin
from wedding.photos.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = "date_uploaded"
    list_display = ('admin_thumbnail', 'title', 'taken_by', 'date_updated')


admin.site.register(Photo, PhotoAdmin)