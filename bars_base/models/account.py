from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from bars_api.models import VirtualField
from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.perms import PerBarPermissionsOrAnonReadOnly


class Account(models.Model):
    class Meta:
        unique_together = (("bar", "owner"))
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.FloatField(default=0)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.owner.username + " (" + self.bar.id + ")"

    def save(self, *args, **kwargs):
        if not self.pk:
            Role.objects.create(name='customer', bar=self.bar, user=self.owner)

        super(Account, self).save(*args, **kwargs)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        read_only_fields = ('bar', 'money', 'last_modified')
        extra_kwargs = {'bar': {'required': False}}
    _type = VirtualField("Account")

    def get_validators(self):
        validators = super(AccountSerializer, self).get_validators()
        return filter(lambda v:not isinstance(v, UniqueTogetherValidator), validators)

    def create(self, data):
        request = self.context['request']
        bar = request.QUERY_PARAMS.get('bar', None)
        bar = Bar.objects.get(pk=bar)

        account = Account(**data)
        account.money = 0
        account.bar = bar
        account.save()
        return account


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'owner': ['exact'],
        'bar': ['exact'],
        'money': ['lte', 'gte']}

    @decorators.list_route(methods=['get'])
    def me(self, request):
        bar = request.QUERY_PARAMS.get('bar', None)
        if bar is None:
            serializer = self.serializer_class(request.user.account_set.all())
        else:
            serializer = self.serializer_class(request.user.account_set.get(bar=bar))
        return Response(serializer.data)
