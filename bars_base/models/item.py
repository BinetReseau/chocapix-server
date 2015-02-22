from django.db import models
from rest_framework import viewsets, serializers, permissions

from bars_django.utils import VirtualField
from bars_core.models.bar import Bar
from bars_core.perms import PerBarPermissionsOrAnonReadOnly



class ItemDetails(models.Model):
    class Meta:
        app_label = 'bars_base'
    barcode = models.CharField(max_length=25, blank=True)
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100, blank=True)
    keywords = models.CharField(max_length=200, blank=True)  # Todo: length

    unit_name = models.CharField(max_length=100, blank=True)
    unit_name_plural = models.CharField(max_length=100, blank=True)
    unit_value = models.FloatField(default=1)

    def __unicode__(self):
        return self.name


class ItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDetails
    _type = VirtualField("ItemDetails")


class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = ItemDetails.objects.all()
    serializer_class = ItemDetailsSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary
    filter_fields = {
        'barcode': ['exact']}
    search_fields = ('name', 'keywords')



class Item(models.Model):
    class Meta:
        app_label = 'bars_base'
    bar = models.ForeignKey(Bar)
    details = models.ForeignKey(ItemDetails)
    qty = models.FloatField(default=0)

    unit_name = models.CharField(max_length=100, blank=True)
    unit_name_plural = models.CharField(max_length=100, blank=True)
    unit_value = models.FloatField(default=1)

    buy_price = models.FloatField(default=1)
    price = models.FloatField()
    tax = models.FloatField(default=0)

    deleted = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s)" % (self.details.name, self.bar.id)

    def get_sell_price(self):
        return self.price * (1 + self.tax)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = ('bar', 'qty', 'last_modified')
    _type = VirtualField("Item")

    def create(self, data):
        request = self.context['request']

        item = Item(**data)
        item.qty = 0
        item.bar = request.bar
        item.save()
        return item


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'details': ['exact'],
        'deleted': ['exact']}
