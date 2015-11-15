from django.http import Http404
from django.db import models
from django.db.models import Sum, F, Prefetch, Value as V
from rest_framework import viewsets, serializers, decorators
from bars_django.utils import VirtualField, permission_logic
from rest_framework.response import Response

from bars_core.perms import RootBarRolePermissionLogic, RootBarPermissionsOrAnonReadOnly
from bars_items.models.stockitem import StockItem


class ItemDetailsManager(models.Manager):
    def get_queryset(self):
        return super(ItemDetailsManager, self).get_queryset().prefetch_related(Prefetch('stockitem_set', queryset=StockItem.objects.select_related('bar')))


@permission_logic(RootBarRolePermissionLogic())
class ItemDetails(models.Model):
    class Meta:
        app_label = 'bars_items'
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    container = models.CharField(max_length=100, blank=True)
    container_plural = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=100, blank=True)
    unit_plural = models.CharField(max_length=100, blank=True)
    container_qty = models.FloatField(default=1)
    ranking_unit = models.CharField(max_length=100, blank=True)
    ranking_unit_factor = models.FloatField(default=1)

    keywords = models.CharField(max_length=200, blank=True)  # Todo: length

    objects = ItemDetailsManager()

    def __unicode__(self):
        return self.name


class ItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDetails
    _type = VirtualField("ItemDetails")

    def to_representation(self, itemdetails):
        obj = super(ItemDetailsSerializer, self).to_representation(itemdetails)

        if 'request' in self.context.keys():
            bar = self.context['request'].query_params.get('bar', None)
            if bar is not None:
                stockitems = itemdetails.stockitem_set.all()
                stockitem = next((item for item in stockitems if item.bar.id == bar), None)
                if stockitem is not None:
                    obj["stockitem"] = stockitem.id
                else:
                    obj["stockitem"] = None

        return obj


class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = ItemDetails.objects.all()
    serializer_class = ItemDetailsSerializer
    permission_classes = (RootBarPermissionsOrAnonReadOnly,)
    search_fields = ('name', 'keywords')

    def list(self, request):
        serializer = ItemDetailsSerializer(self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = ItemDetails.objects.get(pk=pk)
        except ItemDetails.DoesNotExist:
            return Http404()

        serializer = ItemDetailsSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @decorators.detail_route()
    def stats(self, request, pk):
        from bars_stats.utils import compute_transaction_stats
        f = lambda qs: qs.filter(itemoperation__target__sellitem=pk)
        aggregate = Sum(F('itemoperation__delta') * V(1)) # TODO: change if buy_unit

        stats = compute_transaction_stats(request, f, aggregate)
        return Response(stats, 200)
