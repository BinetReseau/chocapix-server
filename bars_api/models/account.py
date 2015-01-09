from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.models.user import User

class Account(models.Model):
    class Meta:
        unique_together = (("bar", "owner"))
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.DecimalField(max_digits=8, decimal_places=3)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.owner.username + " (" + self.bar.id + ")"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
    _type = VirtualField("Account")
    money = serializers.FloatField()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_fields = {
        'owner': ['exact'],
        'bar': ['exact'],
        'money': ['lte', 'gte']}

    @decorators.list_route(methods=['get'])
    def me(self, request):
        # Todo: bar
        serializer = self.serializer_class(request.user.account_set.get(bar=Bar.objects.all()[0]))
        return Response(serializer.data)
