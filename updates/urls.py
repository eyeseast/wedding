from django.conf.urls.defaults import *
from django.views.generic import list_detail

from wedding.updates.models import Update

updates_info_dict = {
    'queryset': Update.objects.live(),
    'paginate_by': 20
}

urlpatterns = patterns('',
    url(r'^$',
        list_detail.object_list,
        updates_info_dict,
        name="updates_update_list"
        ),
    
    url(r'^(?P<object_id>\d+)/$',
        list_detail.object_detail,
        {'queryset': Update.objects.live()},
        name="updates_update_detail"
        )
)