from datetime import date, timedelta
from mock import Mock
from django.db import models
from rest_framework import viewsets, serializers, decorators
from rest_framework.response import Response

from bars_django.utils import VirtualField, permission_logic
from bars_core.perms import RootBarRolePermissionLogic


@permission_logic(RootBarRolePermissionLogic())
class Bar(models.Model):
    class Meta:
        app_label = 'bars_core'
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id

    def save(self, *args, **kwargs):
        super(Bar, self).save(*args, **kwargs)
        from bars_core.models.bar import BarSettings
        BarSettings.objects.get_or_create(bar=self)


    def apply_agios(self, account):
        if account.money >= 0 and account.overdrawn_since is not None:
            account.overdrawn_since = None
            account.save()

        elif account.money < 0:
            if account.overdrawn_since is None:
                account.overdrawn_since = date.today()
                account.save()

            if self.settings.agios_enabled and date.today() - account.overdrawn_since >= timedelta(self.settings.agios_threshold):
                delta = abs(account.money) * self.settings.agios_factor
                makeAgiosTransaction(self, account, delta)
                return delta

        return 0

    def count_accounts(self):
        return self.account_set.count()


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
    settings = serializers.PrimaryKeyRelatedField(read_only=True)
    count_accounts = serializers.IntegerField()


from bars_core.perms import RootBarPermissionsOrAnonReadOnly
class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = (RootBarPermissionsOrAnonReadOnly,)

    @decorators.detail_route(methods=['get'])
    def sellitem_ranking(self, request, pk):
        from bars_items.models.sellitem import SellItem
        from bars_stats.utils import compute_ranking
        from django.db.models import Count, Sum, F
        f = {
            'stockitems__itemoperation__transaction__bar': pk,
            'stockitems__itemoperation__transaction__type__in': ("buy", "meal"), 
            'stockitems__deleted': False
        }
        ann = Count('stockitems__itemoperation__transaction')/Count('stockitems', distinct=True)
        ranking = compute_ranking(request, model=SellItem, t_path='stockitems__itemoperation__transaction__', filter=f, annotate=ann)
        if ranking is None:
            return HttpResponseBadRequest("I can only give a ranking within a bar")
        else:
            ranking = ranking.annotate(total=Sum(F('stockitems__itemoperation__delta') * F('stockitems__itemoperation__target__unit_factor')))
            return Response(ranking, 200)

    @decorators.list_route(methods=['get'])
    def nazi_ranking(self, request):
        from bars_stats.utils import compute_ranking
        f = {
            'transaction__type': "punish"
        }
        ann = models.Sum('transaction__moneyflow')
        ranking = compute_ranking(request, model=Bar, t_path='transaction__', filter=f, annotate=ann, all_bars=True)
        return Response(ranking, 200)

    # @decorators.list_route(methods=['get'])
    # def items_ranking(self, request):
    #     from bars_stats.utils import compute_ranking

    #     items = request.query_params.getlist("item")
    #     if len(items) == 0:
    #         return HttpResponseBadRequest("Give me some items to compare bars with")

    #     f = {
    #         'transaction__type__in': ("buy", "meal"),
    #         'transaction__itemoperation__target__details__in': items
    #     }
    #     ann = models.Count('transaction')
    #     ranking = compute_ranking(request, model=Bar, t_path='transaction__', filter=f, annotate=ann, all_bars=True)
    #     return Response(ranking, 200)



from bars_core.perms import BarRolePermissionLogic, PerBarPermissionsOrAnonReadOnly

@permission_logic(BarRolePermissionLogic())
class BarSettings(models.Model):
    class Meta:
        app_label = 'bars_core'
    bar = models.OneToOneField(Bar, primary_key=True, related_name="settings")

    next_scheduled_appro = models.DateTimeField(null=True)
    money_warning_threshold = models.FloatField(default=15)
    transaction_cancel_threshold = models.FloatField(default=48)  # In hours

    agios_enabled = models.BooleanField(default=True)
    agios_threshold = models.FloatField(default=2)  # In days
    agios_factor = models.FloatField(default=0.05)

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.bar.id


class BarSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarSettings
    _type = VirtualField("BarSettings")
    id = serializers.PrimaryKeyRelatedField(read_only=True, source='bar')  # To help the client
    bar = serializers.PrimaryKeyRelatedField(read_only=True)


class BarSettingsViewSet(viewsets.ModelViewSet):
    queryset = BarSettings.objects.all()
    serializer_class = BarSettingsSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)

