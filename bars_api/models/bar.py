from django.db import models
from rest_framework import viewsets, serializers
from bars_api.models import VirtualField


class Bar(models.Model):
    class Meta:
        app_label = 'bars_api'
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
    _type = VirtualField("Bar")


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
