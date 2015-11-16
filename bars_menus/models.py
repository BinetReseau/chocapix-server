from django.db import models
from django.http import Http404

from rest_framework import serializers, viewsets
from rest_framework.response import Response

from bars_django.utils import VirtualField, permission_logic, CurrentBarCreateOnlyDefault, CurrentUserCreateOnlyDefault
from bars_core.perms import BarRolePermissionLogic, PerBarPermissionsOrObjectPermissionsOrAnonReadOnly
from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_items.models.sellitem import SellItem
from bars_menus.perms import MenuOwnerPermissionLogic


ERROR_MESSAGES = {
    'negative': "%(field)s must be positive",
    'wrong_bar': "%(model)s (id=%(id)d) is in the wrong bar",
    'deleted': "%(model)s (id=%(id)d) is deleted"
}

class MenuManager(models.Manager):
    def get_queryset(self):
        return super(MenuManager, self).get_queryset().prefetch_related(
            'items'
        )


@permission_logic(BarRolePermissionLogic())
@permission_logic(MenuOwnerPermissionLogic(field_name='user', delete_permission=True))
class Menu(models.Model):
    class Meta:
        unique_together = ('bar', 'user', 'name', )
    name = models.CharField(max_length=100)
    bar = models.ForeignKey(Bar)
    user = models.ForeignKey(User)

    objects = MenuManager()

    def __unicode__(self):
        user = self.user.pseudo or (self.user.firstname + " " + self.user.lastname)
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
    _type = VirtualField("Menu")
    items = MenuSellItemSerializer(many=True)
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserCreateOnlyDefault())

    class Meta:
        model = Menu
        read_only_fields = ('bar', 'user', )

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
    permission_classes = (PerBarPermissionsOrObjectPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'user': ['exact']
    }
