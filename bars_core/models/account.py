from datetime import datetime, timedelta

from django.db import models
from django.http import HttpResponseBadRequest

from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_django.utils import VirtualField, permission_logic, CurrentBarCreateOnlyDefault
from bars_core.models.bar import Bar
from bars_core.models.user import User, get_default_user
from bars_core.models.role import Role
from bars_core.perms import PerBarPermissionsOrAnonReadOnly, BarRolePermissionLogic


@permission_logic(BarRolePermissionLogic())
class Account(models.Model):
    class Meta:
        unique_together = ("bar", "owner")
        index_together = ["bar", "owner"] # Redundant ?
        app_label = 'bars_core'
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.FloatField(default=0)

    overdrawn_since = models.DateField(null=True) # set to date value when money becomes negative
    deleted = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.owner.get_full_name() + " (" + self.bar.id + ")"

    def save(self, *args, **kwargs):
        if not self.pk:
            Role.objects.get_or_create(name='customer', bar=self.bar, user=self.owner)
        super(Account, self).save(*args, **kwargs)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        read_only_fields = ('bar', 'money', 'overdrawn_since', 'last_modified')

    _type = VirtualField("Account")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'owner': ['exact'],
        'owner__username': ['exact'],
        'bar': ['exact'],
        'money': ['lte', 'gte']}

    @decorators.list_route(methods=['get'])
    def me(self, request):
        """
        Return the account of current user in current bar, if specified, or all accounts of current user otherwise.
        ---
        parameters:
            - name: bar
              required: false
              type: string
              paramType: query
        """
        bar = request.bar
        if bar is None:
            serializer = self.serializer_class(request.user.account_set.all(), many=True)
        else:
            serializer = self.serializer_class(request.user.account_set.get(bar=bar))
        return Response(serializer.data)

    @decorators.detail_route()
    def stats(self, request, pk):
        """
        Return consumption stats of the given account (pk).
        Response format: [["*date*": value, ...], ...]
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: false
              type: string
              paramType: query
            - name: type
              required: false
              type: string
              description: The types of transactions to consider in stats computing (type=buy&type=meal&...)
              paramType: query
            - name: interval
              required: false
              type: string
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from bars_stats.utils import compute_transaction_stats
        f = lambda qs: qs.filter(accountoperation__target=pk)
        aggregate = models.Sum('accountoperation__delta')

        stats = compute_transaction_stats(request, f, aggregate)
        return Response(stats, 200)

    @decorators.detail_route()
    def total_spent(self, request, pk):
        """
        Return total spent money by the given account (pk).
        Response format: {"total_spent": value}
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: false
              type: string
              paramType: query
            - name: type
              required: false
              type: string
              description: The types of transactions to consider in computing (type=buy&type=meal&...)
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from bars_stats.utils import compute_total_spent
        f = lambda qs: qs.filter(accountoperation__target=pk)

        stats = compute_total_spent(request, f)
        return Response(stats, 200)

    @decorators.list_route(methods=['get'])
    def ranking(self, request):
        """
        Return a ranking of all accounts in the bar, according to given rules.
        Response format: [{"id": id, "val": value}, ...]
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: true
              type: string
              paramType: query
            - name: type
              required: false
              type: string
              description: The types of transactions to consider in ranking (type=buy&type=meal&...)
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from bars_stats.utils import compute_ranking
        ranking = compute_ranking(request, annotate=models.Sum('accountoperation__delta'))
        if ranking is None:
            return Response("I can only give a ranking within a bar", 400)
        else:
            return Response(ranking, 200)

    @decorators.list_route(methods=['get'])
    def coheze_ranking(self, request):
        """
        Return a ranking of all accounts in the bar, according to consumption in MealTransaction and other given rules.
        Response format: [{"id": id, "val": value}, ...]
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: true
              type: string
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from django.db.models import Sum, Count, Prefetch
        from bars_transactions.models import Transaction

        bar = request.query_params.get('bar', None)
        t_filter = {}
        if bar is None:
            return Response("I can only give a ranking within a bar", 400)
        else:
            t_filter['bar'] = bar

        t_filter['canceled'] = False

        date_start = request.query_params.get('date_start')
        date_end = request.query_params.get('date_end', datetime.now())
        if date_start is not None:
            t_filter['timestamp__range'] = (date_start, date_end)

        t_filter['type'] = "meal"

        # Ensure that the MealTransaction involves at least 2 accounts (to avoid cheating...)
        admissible_transactions = list(Transaction.objects.filter(**t_filter).annotate(nb_accounts=Count('accountoperation__target')).filter(nb_accounts__gte=2).values('id'))
        admissible_transactions = [t['id'] for t in admissible_transactions]

        ranking = Account.objects.filter(bar=bar, accountoperation__transaction__id__in=admissible_transactions).values('id').annotate(val=Sum('accountoperation__delta'))
        return Response(ranking, 200)

    @decorators.detail_route(methods=['get'])
    def sellitem_ranking(self, request, pk):
        """
        Return a ranking of most consumed SellItems by the account, according to given rules.
        Response format: [{"total": total, "id": id, "val": value}, ...]
        id: SellItem.id
        total: total qty (in SellItem unit)
        val: count of purchase
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: true
              type: string
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from bars_items.models.sellitem import SellItem
        from bars_stats.utils import compute_ranking
        f = {
            'stockitems__itemoperation__transaction__accountoperation__target': pk,
            'stockitems__itemoperation__transaction__type__in': ("buy", "meal"),
            'stockitems__deleted': False
        }
        # Clean request.query_params to avoid conflicts in filtering
        # TODO: find a workaround
        # request.query_params.setlist('type', [])

        if request.bar is None:
            return Response("I can only give a ranking within a bar", 400)

        ann = models.Count('stockitems__itemoperation__transaction')/models.Count('stockitems', distinct=True)
        # Compute ranking according to count of purchase
        ranking = compute_ranking(request, model=SellItem, t_path='stockitems__itemoperation__transaction__', filter=f, annotate=ann)
        # Annotate ranking with quantities
        ranking = ranking.annotate(total=models.Sum(models.F('stockitems__itemoperation__delta') * models.F('stockitems__itemoperation__target__unit_factor') * models.F('stockitems__itemoperation__transaction__accountoperation__delta') / models.F('stockitems__itemoperation__transaction__moneyflow')))
        return Response(ranking, 200)

    @decorators.detail_route(methods=['get'])
    def magicbar_ranking(self, request, pk):
        """
        Return a ranking of preferred SellItems of the given account, weighted by recent purchases.
        Response format: [{"id": id, "val": value}, ...]
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: true
              type: string
              paramType: query
            - name: type
              required: false
              type: string
              description: The types of transactions to consider in ranking (type=buy&type=meal&...)
              paramType: query
        """
        from bars_items.models.sellitem import SellItem
        from bars_stats.utils import compute_ranking
        f = {
            'stockitems__itemoperation__transaction__accountoperation__target': pk,
            #'stockitems__itemoperation__transaction__type__in': ("buy", "meal"),
            'stockitems__deleted': False
        }
        ann = models.Count('stockitems__itemoperation__transaction')/models.Count('stockitems', distinct=True)

        # Compute three rankings : on last week, on last three months and since account's creation
        week = timedelta(days=7)
        month = timedelta(days=90)
        f_ever, f_month, f_week = f, f.copy(), f.copy()
        f_month['stockitems__itemoperation__transaction__timestamp__range'] = (datetime.now() - month, datetime.now())
        f_week['stockitems__itemoperation__transaction__timestamp__range'] = (datetime.now() - week, datetime.now())

        if request.query_params.get('bar') is None:
            return Response("I can only give a ranking within a bar", 400)

        ranking_ever = compute_ranking(request, model=SellItem, t_path='stockitems__itemoperation__transaction__', filter=f_ever, annotate=ann)
        ranking_month = list(compute_ranking(request, model=SellItem, t_path='stockitems__itemoperation__transaction__', filter=f_month, annotate=ann))
        ranking_week = list(compute_ranking(request, model=SellItem, t_path='stockitems__itemoperation__transaction__', filter=f_week, annotate=ann))

        # Mix rankings with weights : last week counts for 10, last three months count for 5 and ever counts for 1
        ranking = []
        for si in ranking_ever.iterator():
            si_id = si['id']
            si_m = next((t for t in ranking_month if t['id'] == si['id']), None)
            si_w = next((t for t in ranking_week if t['id'] == si['id']), None)
            si_val = si['val']
            si_val += 5 * si_m['val'] if si_m is not None else 0
            si_val += 10 * si_w['val'] if si_w is not None else 0

            ranking.append({'id': si_id, 'val': si_val})

        return Response(ranking, 200)

    @decorators.list_route(methods=['get'])
    def items_ranking(self, request):
        """
        Return a ranking of all accounts in the bar, according to consumption of a set of ItemDetails and to given rules.
        Response format: [{"id": id, "val": value}, ...]
        ---
        omit_serializer: true
        parameters:
            - name: bar
              required: true
              type: string
              paramType: query
            - name: item
              required: true
              type: string
              description: The ids of ItemDetails to consider in ranking (item=13&item=34&...)
              paramType: query
            - name: date_start
              required: false
              type: datetime
              paramType: query
            - name: date_end
              required: false
              type: datetime
              paramType: query
        """
        from bars_stats.utils import compute_ranking
        from django.db.models import Sum, F

        items = request.query_params.getlist("item")
        if len(items) == 0:
            return Response("Give me some items to compare accounts with", 400)

        f = {
            'accountoperation__transaction__type__in': ("buy", "meal"),
            'accountoperation__transaction__itemoperation__target__details__in': items
        }
        ann = Sum(F('accountoperation__transaction__itemoperation__delta') * F('accountoperation__transaction__itemoperation__target__unit_factor'))
        # Compute ranking according to quantities
        ranking = compute_ranking(request, model=Account, t_path='accountoperation__transaction__', filter=f, annotate=ann)
        return Response(ranking, 200)


# default_account_map = {}
def get_default_account(bar):
    """
    Return the account associated to default_user in bar.
    """
    # global default_account_map
    user = get_default_user()
    # if bar.id not in default_account_map:
    #     default_account_map[bar.id], _ = Account.objects.get_or_create(owner=user, bar=bar)
    x, _ = Account.objects.get_or_create(owner=user, bar=bar)
    return x
