from datetime import datetime
from mock import Mock
from django.db import models
from rest_framework import viewsets, serializers, permissions
from bars_django.utils import VirtualField


class Bar(models.Model):
    class Meta:
        app_label = 'bars_core'
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)

    next_scheduled_appro = models.DateTimeField(null=True)
    money_warning_threshold = models.FloatField(default=15)

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

    def apply_agios(self, account):
        if account.money >= 0 and account.overdrawn_since is not None:
            account.overdrawn_since = None
            account.save()

        elif account.money < 0:
            if account.overdrawn_since is None:
                account.overdrawn_since = datetime.now()
                account.save()

            delta = abs(account.money) * 0.05
            makeAgiosTransaction(self, account, delta)
            return delta

        return 0


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
    _type = VirtualField("Bar")


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: temporary


def makeAgiosTransaction(bar, account, amount):
    from bars_transactions.serializers import AgiosTransactionSerializer
    from bars_core.models.user import get_default_user
    user = get_default_user()
    user.has_perm = Mock(return_value=True)
    data = {'type': 'agios', 'account': account.id, 'amount': amount}
    context = {'request': Mock(bar=bar, user=user)}

    s = AgiosTransactionSerializer(data=data, context=context)
    s.is_valid(raise_exception=True)
    s.save()
