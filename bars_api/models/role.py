from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.models.user import User


class Role(models.Model):
    class Meta:
        app_label = 'bars_api'
    name = models.CharField(max_length=127)
    bar = models.ForeignKey(Bar)
    user = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)

    def get_permissions(self):
        return []  # TODO

    def __unicode__(self):
        return self.user.username + " : " + self.name + " (" + self.bar.id + ")"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
    _type = VirtualField("Role")
    perms = serializers.ListField(child=serializers.CharField(max_length=127), read_only=True, source='get_permissions')



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
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
