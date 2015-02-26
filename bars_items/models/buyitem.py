from django.http import Http404
from django.db import models
from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response

from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault
from bars_core.models.bar import Bar
# from bars_core.perms import PerBarPermissionsOrAnonReadOnly
from bars_items.models.itemdetails import ItemDetails


class BuyItem(models.Model):
    class Meta:
        app_label = 'bars_items'
    barcode = models.CharField(max_length=25, blank=True)
    details = models.ForeignKey(ItemDetails)
    itemqty = models.FloatField(default=1)

    def __unicode__(self):
        return "%s * %f %s" % (unicode(self.details), self.itemqty * self.details.unit_value, self.details.unit_name)

class BuyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyItem
    _type = VirtualField("BuyItem")


class BuyItemViewSet(viewsets.ModelViewSet):
    queryset = BuyItem.objects.all()
    serializer_class = BuyItemSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['barcode', 'details']



class BuyItemPrice(models.Model):
    class Meta:
        unique_together = ("bar", "buyitem")
        app_label = 'bars_items'
    bar = models.ForeignKey(Bar)
    buyitem = models.ForeignKey(BuyItem)
    price = models.FloatField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.buyitem), unicode(self.bar))


class BuyItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyItemPrice
        read_only_fields = ("bar",)

    _type = VirtualField("BuyItemPrice")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())


class BuyItemPriceViewSet(viewsets.ModelViewSet):
    queryset = BuyItemPrice.objects.all()
    serializer_class = BuyItemPriceSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar', 'buyitem']

    def create(self, request):
        bar = request.bar
        barcode = request.data.get('barcode', None)

        if barcode is None:
            return Response('No barcode specified', 400)
        if bar is None:
            raise Response('No bar specified', 400)

        try:
            buyitem = BuyItem.objects.get(barcode=barcode)
        except BuyItem.DoesNotExist:
            raise Http404('Barcode does not exist')

        buyitemprice, created = BuyItemPrice.objects.get_or_create(bar=bar, buyitem=buyitem)
        if not created:
            return Response('BuyItemPrice exists', 409)

        other_prices = BuyItemPrice.objects.filter(bar=bar, buyitem__details=buyitem.details).exclude(pk=buyitemprice.pk)
        if other_prices.count() != 0:
            price = sum([bip.price * bip.buyitem.itemqty for bip in other_prices.all()]) / other_prices.count()
        else:
            price = 0

        buyitemprice.price = price / buyitem.itemqty
        buyitemprice.save()

        return Response(BuyItemPriceSerializer(buyitemprice).data, 201)
