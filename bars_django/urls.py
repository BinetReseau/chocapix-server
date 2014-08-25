from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from rest_framework import viewsets, routers
from bars_api.models import User, Account, Bar

router = routers.DefaultRouter()
class UserViewSet(viewsets.ModelViewSet):
    model = User
router.register(r'users', UserViewSet)

class AccountViewSet(viewsets.ModelViewSet):
    model = Account
router.register(r'accounts', AccountViewSet)

class BarViewSet(viewsets.ModelViewSet):
    model = Bar
router.register(r'bars', BarViewSet)



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
)
