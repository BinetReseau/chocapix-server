from django.db import models
from rest_framework import viewsets, serializers, permissions

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
    price = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.details), unicode(self.bar))

    def get_sell_price(self):
        return self.price * (1 + self.sellitem.tax)


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        read_only_fields = ('bar', 'details', 'qty')
    _type = VirtualField("StockItem")

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
