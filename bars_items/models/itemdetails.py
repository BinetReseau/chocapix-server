from django.db import models
from rest_framework import viewsets, serializers, permissions
from bars_django.utils import VirtualField
from bars_items.models.stockitem import StockItem

class ItemDetails(models.Model):
    class Meta:
        app_label = 'bars_items'
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100, blank=True)
    keywords = models.CharField(max_length=200, blank=True)  # Todo: length

    def __unicode__(self):
        return self.name


class ItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDetails
    _type = VirtualField("ItemDetails")

    def to_representation(self, itemdetails):
        obj = super(ItemDetailsSerializer, self).to_representation(itemdetails)

        bar = self.context['request'].bar
        try:
            stockitem = StockItem.objects.get(bar=bar, details=itemdetails)
            obj["stockitem"] = stockitem.id
        except StockItem.DoesNotExist:
            pass

        return obj


class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = ItemDetails.objects.all()
    serializer_class = ItemDetailsSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    search_fields = ('name', 'keywords')
