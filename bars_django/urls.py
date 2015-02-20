from django.conf.urls import patterns, include, url
from rest_framework import routers

from django.contrib import admin
admin.autodiscover()

import permission
permission.autodiscover()

from bars_core.models.bar import BarViewSet
from bars_core.models.user import UserViewSet
from bars_base.models.account import AccountViewSet
from bars_core.models.role import RoleViewSet
from bars_base.models.item import ItemViewSet, ItemDetailsViewSet
from bars_news.models import NewsViewSet
from bars_transactions.views import TransactionViewSet


router = routers.DefaultRouter()

router.register('bar', BarViewSet)
router.register('user', UserViewSet)
router.register('account', AccountViewSet)
router.register('role', RoleViewSet)
router.register('item', ItemViewSet)
router.register('itemdetails', ItemDetailsViewSet)
router.register('news', NewsViewSet)
router.register('transaction', TransactionViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^', include(router.urls)),
)
