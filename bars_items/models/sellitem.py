from django.db import models
from rest_framework import viewsets, serializers, permissions

from bars_django.utils import VirtualField
from bars_core.models.bar import Bar


class SellItem(models.Model):
    class Meta:
        app_label = 'bars_items'
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100, blank=True)

    unit_name = models.CharField(max_length=100, blank=True)
    unit_name_plural = models.CharField(max_length=100, blank=True)
    unit_value = models.FloatField(default=1)

    tax = models.FloatField(default=0)

    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class SellItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellItem
        fields = ("id", "bar", "stockitems", "name", "name_plural", "unit_name", "unit_name_plural", "unit_value", "tax", "_type")
        read_only_fields = ("id", "bar")
    _type = VirtualField("SellItem")


class SellItemViewSet(viewsets.ModelViewSet):
    queryset = SellItem.objects.all()
    serializer_class = SellItemSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar']
