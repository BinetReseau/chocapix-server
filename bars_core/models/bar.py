from datetime import date, timedelta
from mock import Mock
from django.db import models
from rest_framework import viewsets, serializers

from bars_django.utils import VirtualField, permission_logic
from bars_core.perms import RootBarRolePermissionLogic



@permission_logic(RootBarRolePermissionLogic())
class Bar(models.Model):
    class Meta:
        app_label = 'bars_core'
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)

    next_scheduled_appro = models.DateTimeField(null=True)
    money_warning_threshold = models.FloatField(default=15)

    agios_enabled = models.BooleanField(default=True)
    agios_threshold = models.FloatField(default=2)  # In days
    agios_factor = models.FloatField(default=0.05)

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

    def apply_agios(self, account):
        if account.money >= 0 and account.overdrawn_since is not None:
            account.overdrawn_since = None
            account.save()

        elif account.money < 0:
            if account.overdrawn_since is None:
                account.overdrawn_since = date.today()
                account.save()

            if self.agios_enabled and date.today() - account.overdrawn_since >= timedelta(self.agios_threshold):
                delta = abs(account.money) * self.agios_factor
                makeAgiosTransaction(self, account, delta)
                return delta

        return 0


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


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
    _type = VirtualField("Bar")


from bars_core.perms import RootBarPermissionsOrAnonReadOnly
class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = (RootBarPermissionsOrAnonReadOnly,)
