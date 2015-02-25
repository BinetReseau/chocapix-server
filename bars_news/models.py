from django.db import models
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import viewsets
from django.http import Http404

from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault, CurrentUserCreateOnlyDefault
from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.perms import PerBarPermissionsOrAnonReadOnly


class News(models.Model):
    class Meta:
        app_label = 'bars_news'
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
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserCreateOnlyDefault())


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'timestamp': ['lte', 'gte'],
        'author': ['exact']}
    search_fields = ('name', 'text')
