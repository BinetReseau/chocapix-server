from rest_framework import fields
class VirtualField(fields.ReadOnlyField):
    """
    Identify the type of resource that is returned by the API. Needed by client's API Model.
    """
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



from permission import add_permission_logic
def permission_logic(logic):
    """
    Define a model decorator to specify permission logic to apply to the model.
    """
    def decorator(model):
        add_permission_logic(model, logic)
        return model
    return decorator



def get_root_bar():
    """
    Return (and create if needed) a root bar (admin zone).
    """
    if get_root_bar._cache is None:
        from bars_core.models.bar import Bar
        get_root_bar._cache, _ = Bar.objects.get_or_create(id="root", name="Root")
    return get_root_bar._cache
get_root_bar._cache = None



from django.http import Http404
class BarMiddleware(object):
    """
    Define a Django middleware to attach a Bar instance to any request with a GET parameter called "bar".
    """
    def process_request(self, request):
        from bars_core.models.bar import Bar
        bar = request.GET.get('bar', None)
        if bar is None:
            request.bar = None
        else:
            try:
                request.bar = Bar.objects.get(pk=bar)
            except Bar.DoesNotExist:
                raise Http404("Unknown bar: %s" % bar)
        return None



class CurrentUserCreateOnlyDefault:
    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent.instance is not None
        self.user = serializer_field.context['request'].user

    def __call__(self):
        if self.is_update:
            raise fields.SkipField()
        return self.user

class CurrentBarCreateOnlyDefault:
    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent.instance is not None
        self.bar = serializer_field.context['request'].bar

    def __call__(self):
        if self.is_update:
            raise fields.SkipField()
        return self.bar



def get_client_ip(request):
    """
    Return requesting person's IP.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
