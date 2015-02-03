from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.models.user import User


role_map = {}
role_map['customer'] = [
    'bars_api.add_transaction',
    'bars_api.add_buytransaction',
    'bars_api.add_throwtransaction',
    'bars_api.add_givetransaction',
    'bars_api.add_mealtransaction',
]
role_map['newsmanager'] = [
    'bars_api.add_news',
    'bars_api.change_news',
    'bars_api.delete_news',
]
role_map['appromanager'] = [
    'bars_api.add_transaction',
    'bars_api.add_approtransaction',
    'bars_api.add_item',
    'bars_api.change_item',
    # 'bars_api.delete_item',
]
role_map['inventorymanager'] = role_map['appromanager'] + [
    'bars_api.add_transaction',
    'bars_api.add_inventorytransaction',
]
role_map['staff'] = role_map['inventorymanager'] + [
    'bars_api.add_transaction',
    'bars_api.add_deposittransaction',
    'bars_api.add_punishtransaction',
    'bars_api.change_transaction',
]
role_map['admin'] = role_map['staff'] + role_map['newsmanager'] + [
    'bars_api.add_role',
    'bars_api.change_role',
    'bars_api.delete_role',
    'bars_api.add_account',
    'bars_api.change_account',
    'bars_api.delete_account',
]
role_list = list(role_map.keys())


class Role(models.Model):
    class Meta:
        app_label = 'bars_api'
    name = models.CharField(max_length=127, choices=zip(role_list, role_list))
    bar = models.ForeignKey(Bar)
    user = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)

    def get_permissions(self):
        return role_map[self.name] if self.name in role_map else []

    def __unicode__(self):
        return self.user.username + " : " + self.name + " (" + self.bar.id + ")"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
    _type = VirtualField("Role")
    perms = serializers.ListField(child=serializers.CharField(max_length=127), read_only=True, source='get_permissions')


from bars_api.perms import PerBarPermissionsOrAnonReadOnly

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'user': ['exact'],
        'bar': ['exact'],
        'name': ['exact']}

    @decorators.list_route(methods=['get'])
    def me(self, request):
        bar = request.QUERY_PARAMS.get('bar', None)
        if bar is None:
            roles = request.user.role_set.all()
        else:
            roles = request.user.role_set.filter(bar=bar)
        serializer = self.serializer_class(roles)
        return Response(serializer.data)
