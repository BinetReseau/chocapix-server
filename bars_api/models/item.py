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
    qty = models.DecimalField(max_digits=7, decimal_places=3)

    unit = models.CharField(max_length=100, blank=True)
    unit_value = models.DecimalField(max_digits=12, decimal_places=6, default=1)
    buy_unit = models.CharField(max_length=100, blank=True)
    buy_unit_value = models.DecimalField(max_digits=12, decimal_places=6, default=1)

    price = models.DecimalField(max_digits=7, decimal_places=3, default=1)
    buy_price = models.DecimalField(max_digits=7, decimal_places=3, default=1)

    deleted = models.BooleanField(default=False)
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
