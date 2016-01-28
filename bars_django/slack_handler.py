import requests

from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

class SlackHandler(AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
            filter = get_exception_reporter_filter(request)
            request_repr = '\n{0}'.format(filter.get_request_repr(request))
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
            request_repr = "unavailable"
        subject = self.format_subject(subject)

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        title = self.format(record).split("\n")[0]
        message = "```\n%s\n\nRequest repr(): %s\n```" % (self.format(record), request_repr)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        html_message = reporter.get_traceback_html() if self.include_html else None
        proxies = settings.PROXIES

        requests.post(settings.SLACK_WEBHOOK_ERROR_URL, json={
            "attachments": [{
                "fallback": "*" + title +"*",
                "pretext": "*" + title +"*",
                "color": "#ef2a2a",
                "text": message,
                "mrkdwn_in": ["pretext", "text"]
            }]
        }, proxies=proxies)
