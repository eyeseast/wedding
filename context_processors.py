from django.contrib.flatpages.models import FlatPage

def flatpage_processor(request):
    "Simple processor that just puts all FlatPage objects into context"
    return {'flatpages': FlatPage.objects.all()}