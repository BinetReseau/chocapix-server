from django.http import Http404
from django.db import models
from django.db.models import Prefetch
from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.fields import CreateOnlyDefault

from bars_django.utils import VirtualField, permission_logic, CurrentBarCreateOnlyDefault
from bars_core.perms import PerBarPermissionsOrAnonReadOnly, BarRolePermissionLogic, RootBarRolePermissionLogic, RootBarPermissionsOrAnonReadOnly
from bars_core.models.bar import Bar
from bars_items.models.itemdetails import ItemDetails


@permission_logic(BarRolePermissionLogic())
class BuyItemPrice(models.Model):
    class Meta:
        unique_together = ("bar", "buyitem")
        app_label = 'bars_items'
    bar = models.ForeignKey(Bar)
    buyitem = models.ForeignKey('BuyItem')
    price = models.FloatField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.buyitem), unicode(self.bar))


@permission_logic(RootBarRolePermissionLogic())
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

        if 'request' in self.context.keys() and self.context.get('request').method == 'GET':
            bar = self.context['request'].query_params.get('bar', None)
            if bar is not None:
                try:
                    obj["buyitemprice"] = buyitem.buyitemprice[0].id
                except IndexError:
                    obj["buyitemprice"] = None
        else:
            try:
                bar = self.context['request'].bar
                buyitemprice = BuyItemPrice.objects.get(bar=bar, buyitem=buyitem)
                obj["buyitemprice"] = buyitemprice.id
            except (KeyError, BuyItemPrice.DoesNotExist):
                pass

        return obj


class BuyItemViewSet(viewsets.ModelViewSet):
    queryset = BuyItem.objects.all()
    serializer_class = BuyItemSerializer
    permission_classes = (RootBarPermissionsOrAnonReadOnly,)
    filter_fields = ['barcode', 'details']

    def list(self, request):
        bar = request.query_params.get('bar', None)
        qs = self.filter_queryset(self.get_queryset())

        if bar is None:
            serializer = BuyItemSerializer(qs, many=True)
        else:
            serializer = BuyItemSerializer(qs.prefetch_related(Prefetch('buyitemprice_set', queryset=BuyItemPrice.objects.filter(bar__id=bar), to_attr='buyitemprice')), many=True, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bar = request.query_params.get('bar', None)

        if bar is None:
            qs = self.get_queryset()
        else:
            qs = self.get_queryset().prefetch_related(Prefetch('buyitemprice_set', queryset=BuyItemPrice.objects.filter(bar__id=bar), to_attr='buyitemprice'))

        try:
            instance = qs.get(pk=pk)
        except BuyItem.DoesNotExist:
            return Http404()

        serializer = BuyItemSerializer(instance, context={'request': request})
        return Response(serializer.data)


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
                    raise Http404('Barcode does not exist')

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
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = ['bar', 'buyitem']
