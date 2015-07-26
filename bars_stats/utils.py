# From https://github.com/kmike/django-qsstats-magic
from django.conf import settings
def _guess_engine(qs):
    if hasattr(qs, 'db'): # django 1.2+
        engine_name = settings.DATABASES[qs.db]['ENGINE']
    else:
        engine_name = settings.DATABASE_ENGINE
    if 'mysql' in engine_name:
        return 'mysql'
    if 'postg' in engine_name: #postgres, postgis
        return 'postgresql'
    if 'sqlite' in engine_name:
        return 'sqlite'

# From https://github.com/kmike/django-qsstats-magic
def _get_interval_sql(date_field, interval, engine):
    ''' Returns SQL clause that calculates the beginning of interval
        date_field belongs to.
    '''

    SQL = {
        'mysql': {
            'minutes': "DATE_FORMAT(`" + date_field +"`, '%%Y-%%m-%%d %%H:%%i')",
            'hours': "DATE_FORMAT(`" + date_field +"`, '%%Y-%%m-%%d %%H:00')",
            'days': "DATE_FORMAT(`" + date_field +"`, '%%Y-%%m-%%d')",
            'weeks': "DATE_FORMAT(DATE_SUB(`"+date_field+"`, INTERVAL(WEEKDAY(`"+date_field+"`)) DAY), '%%Y-%%m-%%d')",
            'months': "DATE_FORMAT(`" + date_field +"`, '%%Y-%%m-01')",
            'years': "DATE_FORMAT(`" + date_field +"`, '%%Y-01-01')",
        },
        'postgresql': {
            'minutes': "date_trunc('minute', %s)" % date_field,
            'hours': "date_trunc('hour', %s)" % date_field,
            'days': "date_trunc('day', %s)" % date_field,
            'weeks': "date_trunc('week', %s)" % date_field,
            'months': "date_trunc('month', %s)" % date_field,
            'years': "date_trunc('year', %s)" % date_field,
        },
        'sqlite': {
            'minutes': "strftime('%%Y-%%m-%%d %%H:%%M', `" + date_field + "`)",
            'hours': "strftime('%%Y-%%m-%%d %%H:00', `" + date_field + "`)",
            'days': "strftime('%%Y-%%m-%%d', `" + date_field + "`)",
            'weeks':  "strftime('%%Y-%%m-%%d', julianday(`" + date_field + "`) - strftime('%%w', `" + date_field + "`) + 1)",
            'months': "strftime('%%Y-%%m-01', `" + date_field + "`)",
            'years': "strftime('%%Y-01-01', `" + date_field + "`)",
        },
    }

    try:
        engine_sql = SQL[engine]
    except KeyError:
        msg = '%s DB engine is not supported. Supported engines are: %s' % (engine, ", ".join(SQL.keys()))
        raise Exception(msg)

    try:
        return engine_sql[interval]
    except KeyError:
        raise Exception('Interval is not supported for %s DB backend.' % engine)


# Inspired from https://github.com/kmike/django-qsstats-magic
from django.db.models import Count
def time_series(qs, date_field, aggregate=None, interval='days', engine=None):
    aggregate = aggregate or Count('id')
    engine = engine or _guess_engine(qs)

    interval_sql = _get_interval_sql(date_field, interval, engine)
    aggregate_data = qs.extra(select = {'qss_date': interval_sql}).\
                            order_by().values('qss_date').\
                            annotate(qss_agg=aggregate)

    return [(x['qss_date'], x['qss_agg']) for x in aggregate_data]


from bars_transactions.models import Transaction
def compute_transaction_stats(request, filter=id, aggregate=None):
    qs = Transaction.objects.all()
    qs = filter(qs)

    if request.bar:
        qs = qs.filter(bar=request.bar)

    types = request.query_params.getlist("type")
    if len(types) != 0:
        qs = qs.filter(type__in=types)

    qs = qs.order_by('-timestamp', '-id').distinct()

    interval = request.query_params.get('interval', 'days')
    return time_series(qs, date_field='timestamp', interval=interval, aggregate=aggregate)
