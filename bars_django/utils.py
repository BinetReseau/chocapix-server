from rest_framework import fields

class VirtualField(fields.ReadOnlyField):
    type_name = 'VirtualField'
    type_label = 'virtual'
    label = 'virtual'
    source = ''

    def __init__(self, value):
        super(VirtualField, self).__init__()
        self.value = value

    def get_attribute(self, instance):
        return ''

    def to_representation(self, attr):
        return self.value

from django.http import Http404
from bars_core.models.bar import Bar
class BarMiddleware(object):
    def process_request(self, request):
        bar = request.GET.get('bar', None)
        if bar is None:
            request.bar = None
        else:
            try:
                request.bar = Bar.objects.get(pk=bar)
            except Bar.DoesNotExist:
                raise Http404("Unknown bar: %s" % bar)
        return None
