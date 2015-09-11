from django.db import models
from django.http import Http404

from rest_framework import serializers, viewsets
from rest_framework.response import Response

from bars_core.perms import PerBarPermissionsOrAnonReadOnly
from bars_core.models.account import Account
from bars_items.models.sellitem import SellItem


ERROR_MESSAGES = {
    'negative': "%(field)s must be positive",
    'wrong_bar': "%(model)s (id=%(id)d) is in the wrong bar",
    'deleted': "%(model)s (id=%(id)d) is deleted"
}


class Menu(models.Model):
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account)

    def __unicode__(self):
        user = self.account.owner.pseudo or (self.account.owner.firstname + " " + self.account.owner.lastname)
        return "%s (%s)" % (self.name, user)


class MenuSellItem(models.Model):
    menu = models.ForeignKey(Menu, blank=True, related_name='items')
    sellitem = models.ForeignKey(SellItem)
    qty = models.FloatField(default=0)


class MenuSellItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSellItem
        exclude = ('menu', 'id', )

    sellitem = serializers.PrimaryKeyRelatedField(queryset=SellItem.objects.all())
    qty = serializers.FloatField()

    def validate_qty(self, value):
        if value < 0:
            raise ValidationError(ERROR_MESSAGES['negative'] % {'field':"Quantity"})
        return value

    def validate_sellitem(self, item):
        err_params = {'model': 'SellItem', 'id': item.id}
        if item is not None and item.deleted:
            raise ValidationError(ERROR_MESSAGES['deleted'] % err_params)

        if item is not None and self.context['request'].bar.id != item.bar.id:
            raise ValidationError(ERROR_MESSAGES['wrong_bar'] % err_params)

        return item


class MenuSerializer(serializers.ModelSerializer):
    items = MenuSellItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'account', 'items', )

    def create(self, data):
        items = data.pop('items')
        menu = super(MenuSerializer, self).create(data)

        for si_data in items:
            MenuSellItem.objects.create(menu=menu, **si_data)

        return menu

    def update(self, instance, data):
        items = data.pop('items')
        MenuSellItem.objects.filter(menu=instance).delete()
        for si_data in items:
            MenuSellItem.objects.create(menu=instance, **si_data)
        
        return super(MenuSerializer, self).update(instance, data)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)


