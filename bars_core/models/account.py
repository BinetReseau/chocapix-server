from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault
from bars_core.models.bar import Bar
from bars_core.models.user import User, get_default_user
from bars_core.models.role import Role
from bars_core.perms import PerBarPermissionsOrAnonReadOnly


class Account(models.Model):
    class Meta:
        unique_together = ("bar", "owner")
        app_label = 'bars_core'
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.FloatField(default=0)

    deleted = models.BooleanField(default=False)
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

    _type = VirtualField("Account")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())


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
        bar = request.bar
        if bar is None:
            serializer = self.serializer_class(request.user.account_set.all())
        else:
            serializer = self.serializer_class(request.user.account_set.get(bar=bar))
        return Response(serializer.data)


def get_default_account(bar):
    user = get_default_user()
    try:
        return Account.objects.get(owner=user, bar=bar)
    except Account.DoesNotExist:
        return Account.objects.create(owner=user, bar=bar)
