from django.db import models
from rest_framework import viewsets
from rest_framework import serializers

from bars_api.models import VirtualField
from bars_api.models.bar import Bar


class Item(models.Model):
    class Meta:
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200)  # Todo: length
    qty = models.FloatField()

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
    _type = VirtualField("Item")


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_fields = {
        'bar': ['exact'],
        'qty': ['lte', 'gte'],
        'deleted': ['exact']}
    search_fields = ('name', 'keywords')
