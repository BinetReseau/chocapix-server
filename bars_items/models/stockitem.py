from django.db import models
from rest_framework import viewsets, serializers, permissions
from rest_framework.validators import UniqueTogetherValidator

from bars_django.utils import VirtualField
from bars_core.models.bar import Bar
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.sellitem import SellItem


class StockItem(models.Model):
    class Meta:
        unique_together = ("bar", "details")
        app_label = 'bars_items'
    bar = models.ForeignKey(Bar)
    details = models.ForeignKey(ItemDetails)
    sellitem = models.ForeignKey(SellItem, related_name="stockitems")

    qty = models.FloatField(default=0)
    unit_value = models.FloatField(default=1)
    price = models.FloatField()
    buy_price = models.FloatField(default=0)

    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.details), unicode(self.bar))

    def computed_price(self):
        return self.unit_value * self.price * (1 + self.sellitem.tax)


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        read_only_fields = ('bar', 'qty')
        extra_kwargs = {'bar': {'required': False}}

    _type = VirtualField("StockItem")
    computed_price = serializers.FloatField(source='computed_price')

    def get_validators(self):
        validators = super(StockItemSerializer, self).get_validators()
        return filter(lambda v:not isinstance(v, UniqueTogetherValidator), validators)

    def create(self, data):
        request = self.context['request']

        item = StockItem(**data)
        item.qty = 0
        item.bar = request.bar
        item.save()
        return item


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar', 'details', 'sellitem']
