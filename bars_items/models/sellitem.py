from django.http import Http404
from django.db import models
from rest_framework import viewsets, serializers, permissions, decorators, exceptions
from rest_framework.response import Response

from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault
from bars_core.models.bar import Bar


class SellItem(models.Model):
    class Meta:
        app_label = 'bars_items'
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100, blank=True)

    unit_name = models.CharField(max_length=100, blank=True)
    unit_name_plural = models.CharField(max_length=100, blank=True)

    tax = models.FloatField(default=0)

    deleted = models.BooleanField(default=False)

    def calc_qty(self):
        if not hasattr(self, '_qty'):
            self._qty = sum(i.sell_qty for i in self.stockitems.all())
        return self._qty

    def calc_price(self):
        qty = self.calc_qty()
        if qty != 0:
            return sum(i.qty * i.get_price() for i in self.stockitems.all()) / qty
        elif self.stockitems.count() != 0:
            return sum(i.get_price('sell') for i in self.stockitems.all()) / self.stockitems.count()
        else:
            return 0

    def __unicode__(self):
        return self.name


class SellItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellItem
        fields = ("id", "bar", "stockitems", "name", "name_plural", "unit_name", "unit_name_plural", "tax", "deleted", "fuzzy_qty", "fuzzy_price", "_type")
        read_only_fields = ("id", "bar")
        extra_kwargs = {'stockitems': {'required': False}}

    _type = VirtualField("SellItem")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    fuzzy_qty = serializers.FloatField(read_only=True, source='calc_qty')
    fuzzy_price = serializers.FloatField(read_only=True, source='calc_price')





class AddStockItemSerializer(serializers.BaseSerializer):
    sellitem = serializers.PrimaryKeyRelatedField(queryset=SellItem.objects.all())
    unit_factor = serializers.FloatField()

class SellItemViewSet(viewsets.ModelViewSet):
    queryset = SellItem.objects.all()
    serializer_class = SellItemSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = ['bar']

    @decorators.detail_route(methods=['put'])
    def merge(self, request, pk=None):
        unsrz = AddStockItemSerializer(data=request.data)
        unsrz.is_valid(raise_exception=True)
        other = unsrz.validated_data['sellitem']
        unit_factor = unsrz.validated_data['unit_factor']

        try:
            this = SellItem.objects.get(pk=pk)
        except SellItem.DoesNotExist:
            raise Http404('SellItem (id=%d) does not exist' % pk)

        if this.bar != request.bar or other.bar != this.bar or other.bar != request.bar:
            raise exceptions.PermissionDenied('Cannot operate across bars')

        for stockitem in other.stockitems.all():
            stockitem.sellitem = this
            stockitem.unit_factor *= unit_factor
            stockitem.save()
        other.delete()

        srz = SellItemSerializer(this)
        return Response(srz.data, 200)
