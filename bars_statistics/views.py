from django.http import Http404
from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bars_base.models.account import Account
from bars_core.models.bar import Bar
from bars_items.models.sellitem import SellItem

from bars_statistics.serializers import (UsersRankingSerializer, ItemsRankingSerializer,
										UsersRankingByItemSerializer,)


class StatisticsViewSet(viewsets.ViewSet):
	queryset=Bar.objects.all()

	@decorators.list_route(methods=['get'])
	def users_ranking(self, request):
		try:
			bar = Bar.objects.get(id=request.bar)
		except Bar.DoesNotExist:
			raise Http404()

		serializer = UsersRankingSerializer(bar)
		return Response(serializer.data)

	@decorators.list_route(methods=['get'])
	def items_ranking(self, request):
		try:
			bar = Bar.objects.get(id=request.bar)
		except Bar.DoesNotExist:
			raise Http404()

		serializer = ItemsRankingSerializer(bar)
		return Response(serializer.data)

	@decorators.list_route(methods=['get'])
	def users_ranking_by_item(self, request):
		try:
			bar = Bar.objects.get(id=request.bar)
		except Bar.DoesNotExist:
			raise Http404()

		try:
			sellitem = SellItem.objects.get(bar=request.bar, id=request.QUERY_PARAMS.get('sellitem', None))
		except SellItem.DoesNotExist:
			raise Http404()

		serializer = UsersRankingByItemSerializer(bar, item)
		return Response(serializer.data)
