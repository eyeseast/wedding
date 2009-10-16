from django.contrib import admin
from wedding.updates.models import Update

class UpdateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Update, UpdateAdmin)