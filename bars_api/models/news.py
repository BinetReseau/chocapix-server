from django.db import models
from rest_framework import viewsets
from rest_framework import serializers

from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.models.user import User
from bars_api.perms import PerBarPermissionsOrAnonReadOnly


class News(models.Model):
    class Meta:
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    author = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    text = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
    _type = VirtualField("News")


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'timestamp': ['lte', 'gte'],
        'author': ['exact']}
    search_fields = ('name', 'text')
