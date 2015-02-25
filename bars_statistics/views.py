from django.http import Http404
from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bars_base.models.account import Account
from bars_core.models.bar import Bar

from bars_statistics.serializers import UsersRankingSerializer


class StatisticsViewSet(viewsets.ViewSet):
	@decorators.list_route(methods=['get'])
	def users_ranking(self, request):
		try:
			bar = Bar.objects.get(id=request.bar)
		except Bar.DoesNotExist:
			raise Http404()

		serializer = UsersRankingSerializer(bar)
		return Response(serializer.data)
