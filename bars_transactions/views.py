from django.http import Http404
from django.db.models import Q
from rest_framework import viewsets, decorators, exceptions
from rest_framework.response import Response

from bars_core.perms import PerBarPermissionsOrAnonReadOnly
from bars_transactions.models import Transaction
from bars_transactions.serializers import serializers_class_map


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        data = self.request.data
        if "type" in data:
            return serializers_class_map[data["type"]]
        else:
            return serializers_class_map[""]

    def get_queryset(self):
        queryset = Transaction.objects.all()

        bar = self.request.QUERY_PARAMS.get('bar', None)
        if bar is not None:
            queryset = queryset.filter(bar=bar)

        user = self.request.QUERY_PARAMS.get('user', None)
        if user is not None:
            queryset = queryset.filter(
                Q(accountoperation__target__owner=user) |
                Q(author=user)
            )

        account = self.request.QUERY_PARAMS.get('account', None)
        if account is not None:
            queryset = queryset.filter(
                Q(accountoperation__target=account) |
                Q(author__account=account)
            )

        item = self.request.QUERY_PARAMS.get('item', None)
        if item is not None:
            queryset = queryset.filter(itemoperation__target=item)

        stockitem = self.request.QUERY_PARAMS.get('stockitem', None)
        if stockitem is not None:
            queryset = queryset.filter(itemoperation__target=stockitem)

        sellitem = self.request.QUERY_PARAMS.get('sellitem', None)
        if sellitem is not None:
            queryset = queryset.filter(itemoperation__target__sellitem=sellitem)

        type = self.request.QUERY_PARAMS.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)

        queryset = queryset.order_by('-timestamp')
        # queryset = queryset.order_by('-timestamp').distinct('timestamp')

        page = int(self.request.QUERY_PARAMS.get('page', 0))
        if page != 0:
            page_size = int(self.request.QUERY_PARAMS.get('page_size', 10))
            queryset = queryset[(page - 1) * page_size: page * page_size]

        return queryset


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
