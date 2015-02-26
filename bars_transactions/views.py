from django.http import Http404
from django.db.models import Q
from rest_framework import viewsets, decorators, exceptions, filters
from rest_framework.response import Response

from bars_core.perms import PerBarPermissionsOrAnonReadOnly
from bars_transactions.models import Transaction
from bars_transactions.serializers import serializers_class_map


class TransactionFilterBackend(filters.BaseFilterBackend):
    filter_q = {
        'bar': lambda bar: Q(bar=bar),
        'user': lambda user: Q(accountoperation__target__owner=user) | Q(author=user),
        'account': lambda account: Q(accountoperation__target=account) | Q(author__account=account),
        'item': lambda item: Q(itemoperation__target=item),
        'stockitem': lambda stockitem: Q(itemoperation__target=stockitem),
        'sellitem': lambda sellitem: Q(itemoperation__target__sellitem=sellitem),
        'type': lambda t: Q(type=t),
    }

    def filter_queryset(self, request, queryset, view):
        for (param, q) in self.filter_q.items():
            x = request.query_params.get(param, None)
            if x is not None:
                queryset = queryset.filter(q(x))

        queryset = queryset.order_by('-timestamp')
        # queryset = queryset.order_by('-timestamp').distinct('timestamp')

        page = int(request.query_params.get('page', 0))
        if page != 0:
            page_size = int(request.query_params.get('page_size', 10))
            queryset = queryset[(page - 1) * page_size: page * page_size]

        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_backends = (TransactionFilterBackend,)

    def get_serializer_class(self):
        data = self.request.data
        if "type" in data:
            return serializers_class_map[data["type"]]
        else:
            return serializers_class_map[""]


    @decorators.detail_route(methods=['put'])
    def cancel(self, request, pk=None):
        try:
            transaction = Transaction.objects.select_related().get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404()

        if request.user.has_perm('bars_transactions.change_transaction', transaction):
            transaction.canceled = True
            transaction.save()

            for aop in transaction.accountoperation_set.all():
                aop.propagate()

            for iop in transaction.itemoperation_set.all():
                iop.propagate()

            serializer = self.get_serializer_class()(transaction)
            return Response(serializer.data)

        else:
            raise exceptions.PermissionDenied()

    @decorators.detail_route(methods=['put'])
    def restore(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404()

        if request.user.has_perm('bars_transactions.change_transaction', transaction):
            transaction.canceled = False
            transaction.save()

            for aop in transaction.accountoperation_set.all():
                aop.propagate()

            for iop in transaction.itemoperation_set.all():
                iop.propagate()

            serializer = self.get_serializer_class()(transaction)
            return Response(serializer.data)

        else:
            raise exceptions.PermissionDenied()
