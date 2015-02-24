from django.db import models
from rest_framework import viewsets, serializers, permissions
from rest_framework.validators import UniqueTogetherValidator

from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault
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
    unit_factor = models.FloatField(default=1)
    price = models.FloatField()

    deleted = models.BooleanField(default=False)

    def get_unit(self, unit=''):
        return {'':1, 'sell':self.unit_factor, 'buy':1}[unit]

    def get_price(self, unit=''):
        return self.price * (1 + self.sellitem.tax) / self.get_unit(unit)

    def create_operation(self, delta=None, next_value=None, unit='', **kwargs):
        from bars_transactions.models import ItemOperation
        delta = delta * self.get_unit(unit) if delta else None
        next_value = next_value * self.get_unit(unit) if next_value else None
        io = ItemOperation(target=self, delta=delta, **kwargs)
        io.save()
        return io


    def sell_price(self):
        return self.get_price(unit='sell')

    def sell_qty(self):
        return self.qty * self.get_unit('sell')

    def sell_to_buy(self):
        return self.get_unit('buy') / self.get_unit('sell')

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.details), unicode(self.bar))


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        exclude = ('unit_factor',)

    _type = VirtualField("StockItem")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    qty = serializers.FloatField(source='sell_qty', read_only=True)
    price = serializers.FloatField(source='sell_price')
    sell_to_buy = serializers.FloatField()


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar', 'details', 'sellitem']
