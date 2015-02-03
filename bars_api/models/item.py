from django.db import models
from django.http import Http404
from rest_framework import viewsets
from rest_framework import serializers

from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.perms import PerBarPermissionsOrAnonReadOnly


class Item(models.Model):
    class Meta:
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200, blank=True)  # Todo: length
    qty = models.FloatField(default=0)

    unit = models.CharField(max_length=100, blank=True)
    unit_value = models.FloatField(default=1)
    buy_unit = models.CharField(max_length=100, blank=True)
    buy_unit_value = models.FloatField(default=1)

    price = models.FloatField()
    buy_price = models.FloatField(default=1)  # Todo: temporary

    deleted = models.BooleanField(default=False)
    unavailable = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = ('bar', 'qty', 'last_modified')
    _type = VirtualField("Item")

    def create(self, data):
        request = self.context['request']
        bar = request.QUERY_PARAMS.get('bar', None)
        try:
            bar = Bar.objects.get(pk=bar)

            item = Item(**data)
            item.qty = 0
            item.bar = bar
            item.save()
            return item
        except:
            raise Http404("Unknown bar " + bar)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'qty': ['lte', 'gte'],
        'deleted': ['exact']}
    search_fields = ('name', 'keywords')
