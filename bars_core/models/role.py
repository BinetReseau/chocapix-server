from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_django.utils import VirtualField, permission_logic, get_root_bar, CurrentBarCreateOnlyDefault
from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.perms import PerBarPermissionsOrAnonReadOnly, BarRolePermissionLogic

from bars_core.roles import roles_map, root_roles_map, roles_list

class RoleManager(models.Manager):
    def get_queryset(self):
        return super(RoleManager, self).get_queryset().select_related('bar', 'user')


@permission_logic(BarRolePermissionLogic())
class Role(models.Model):
    class Meta:
        app_label = 'bars_core'
    name = models.CharField(max_length=127, choices=zip(roles_list, roles_list))
    bar = models.ForeignKey(Bar)
    user = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)

    objects = RoleManager()

    def get_permissions(self):
        if self.bar == get_root_bar():
            rmap = root_roles_map
        else:
            rmap = roles_map
        return sorted(set(rmap[self.name])) if self.name in rmap else []

    def __unicode__(self):
        return self.user.username + " : " + self.name + " (" + self.bar.id + ")"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
    _type = VirtualField("Role")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    perms = serializers.ListField(child=serializers.CharField(max_length=127), read_only=True, source='get_permissions')


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
        bar = request.bar
        if bar is None:
            roles = request.user.role_set.all()
        else:
            roles = request.user.role_set.filter(bar=bar)
        serializer = self.serializer_class(roles)
        return Response(serializer.data)
