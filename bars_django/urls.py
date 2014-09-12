from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from rest_framework import viewsets, routers, mixins, status
from bars_api.models import *

router = routers.DefaultRouter()
for (name, model) in {
			'user':User,
			'bar':Bar,
			'account':Account,
			'item':Item,
			'accountoperation':AccountOperation,
			'itemoperation':ItemOperation,
			'transaction':Transaction
		}.items():
	router.register(name, type("ViewSet", (viewsets.ModelViewSet,), {"model":model}))



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
)
