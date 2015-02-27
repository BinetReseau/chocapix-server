from django.http import Http404
from django.db import models
from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.fields import CreateOnlyDefault

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
        return "%s * %f" % (unicode(self.details), self.itemqty)


class BuyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyItem
    _type = VirtualField("BuyItem")

    def to_representation(self, buyitem):
        obj = super(BuyItemSerializer, self).to_representation(buyitem)

        bar = self.context['request'].bar
        try:
            buyitemprice = BuyItemPrice.objects.get(bar=bar, buyitem=buyitem)
            obj["buyitemprice"] = buyitemprice.id
        except BuyItemPrice.DoesNotExist:
            pass

        return obj


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
    barcode = serializers.CharField(required=False, write_only=True)
    buyitem = serializers.PrimaryKeyRelatedField(required=False, default=CreateOnlyDefault(None), queryset=BuyItem.objects.all())
    price = serializers.FloatField(required=False)

    def validate_price(self, price):
        if price is not None and price < 0:
            raise ValidationError("Price must be positive")
        return price

    def validate(self, data):
        if data.get('barcode') is not None:
            if data.get('buyitem') is None:
                try:
                    data['buyitem'] = BuyItem.objects.get(barcode=data['barcode'])
                except BuyItem.DoesNotExist:
                    raise ValidationError('Barcode does not exist')

            if 'barcode' in data:
                data.pop('barcode')

        return data

    def create(self, data):
        if data.get('buyitem') is None and data.get('barcode') is None:
                raise ValidationError("Specify a barcode or a buyitem")

        buyitemprice = super(BuyItemPriceSerializer, self).create(data)
        bar = buyitemprice.bar
        buyitem = buyitemprice.buyitem

        if "price" not in data:
            other_prices = BuyItemPrice.objects.filter(bar=bar, buyitem__details=buyitem.details).exclude(pk=buyitemprice.pk)
            if other_prices.count() != 0:
                price = sum([bip.price / bip.buyitem.itemqty for bip in other_prices.all()]) / other_prices.count()

                buyitemprice.price = price * buyitem.itemqty
                buyitemprice.save()

        return buyitemprice


class BuyItemPriceViewSet(viewsets.ModelViewSet):
    queryset = BuyItemPrice.objects.all()
    serializer_class = BuyItemPriceSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar', 'buyitem']
