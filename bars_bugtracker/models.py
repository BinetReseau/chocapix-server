# -*- coding: utf-8 -*-

import requests

from django.db import models
from rest_framework import serializers, viewsets

from bars_django.utils import VirtualField, permission_logic, CurrentBarCreateOnlyDefault, CurrentUserCreateOnlyDefault
from bars_core.perms import PerBarPermissionsOrAnonReadOnly, BarRolePermissionLogic
from bars_core.models.bar import Bar
from bars_core.models.user import User


@permission_logic(BarRolePermissionLogic())
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

    def create(self, data):
        b = super(BugReportSerializer, self).create(data)

        proxies = {
            "http": "http://129.104.247.2:8080/",
            "https": "http://129.104.247.2:8080/"
        }

        payload = {
            "attachments": [
                {
                    "fallback": u"Un bug a été reporté par _%s_ dans le bar _%s_" % (b.author.get_full_name(), b.bar.name),
                    "text": u"Un bug a été reporté par *%s* dans le bar *%s*" % (b.author.get_full_name(), b.bar.name),
                    "color": "#D00000",
                    "fields": [
                        {
                            "title": "Message",
                            "value": b.message,
                            "short": False
                        },
                        {
                            "title": "Contexte",
                            "value": "```%s```" % b.data,
                            "short": False
                        }
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

        url_slack = "https://hooks.slack.com/services/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"

        requests.post(url_slack, json=payload, proxies=proxies)

        return b


class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly,)
    filter_fields = {
        'bar': ['exact'],
        'author': ['exact']}
    search_fields = ('message', 'data')
