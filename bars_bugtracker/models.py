from django.db import models
from rest_framework import exceptions, serializers, viewsets

from bars_core.models.user import User
from bars_django.utils import VirtualField, CurrentBarCreateOnlyDefault, CurrentUserCreateOnlyDefault
from bars_core.perms import PerBarPermissionsOrAnonReadOnly
from bars_core.models.bar import Bar
from bars_core.models.user import User

class BugReport(models.Model):
    bar = models.ForeignKey(Bar)
    author = models.ForeignKey(User)
    message = models.CharField(max_length=1000)
    data = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    fixed = models.BooleanField(default=False)
    _type = VirtualField("BugReport")

    def __unicode__(self):
        return "#%d by %s at %s" % (self.id, unicode(self.author), unicode(self.timestamp))


class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport

    _type = VirtualField("BugReport")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserCreateOnlyDefault())


class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'author': ['exact']}
    search_fields = ('message', 'data')
