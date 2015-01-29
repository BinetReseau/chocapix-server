from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from rest_framework import viewsets, routers, mixins
# Todo: organize imports
from bars_api.models.bar import BarViewSet
from bars_api.models.user import UserViewSet
from bars_api.models.account import AccountViewSet
from bars_api.models.item import ItemViewSet
from bars_api.models.news import NewsViewSet
from bars_api.models.transaction import TransactionViewSet

router = routers.DefaultRouter()

router.register('bar', BarViewSet)
router.register('user', UserViewSet)
router.register('account', AccountViewSet)
router.register('item', ItemViewSet)
router.register('news', NewsViewSet)
router.register('transaction', TransactionViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^', include(router.urls)),
)
