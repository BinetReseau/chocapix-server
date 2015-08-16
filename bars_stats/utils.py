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
            'hours_of_day': "DATE_FORMAT(`" + date_field +"`, '%%H')",
            'days_of_week': "WEEKDAY(`"+date_field+"`)",
            'months_of_year': "DATE_FORMAT(`" + date_field +"`, '%%m')",
        },
        'postgresql': {
            'minutes': "date_trunc('minute', %s)" % date_field,
            'hours': "date_trunc('hour', %s)" % date_field,
            'days': "date_trunc('day', %s)" % date_field,
            'weeks': "date_trunc('week', %s)" % date_field,
            'months': "date_trunc('month', %s)" % date_field,
            'years': "date_trunc('year', %s)" % date_field,
            'hours_of_day': "extract(hour from %s)" % date_field,
            'days_of_week': "extract(dow from %s)" % date_field,
            'months_of_year': "extract(month from %s)" % date_field,
        },
        'sqlite': {
            'minutes': "strftime('%%Y-%%m-%%d %%H:%%M', `" + date_field + "`)",
            'hours': "strftime('%%Y-%%m-%%d %%H:00', `" + date_field + "`)",
            'days': "strftime('%%Y-%%m-%%d', `" + date_field + "`)",
            'weeks':  "strftime('%%Y-%%m-%%d', julianday(`" + date_field + "`) - strftime('%%w', `" + date_field + "`) + 1)",
            'months': "strftime('%%Y-%%m-01', `" + date_field + "`)",
            'years': "strftime('%%Y-01-01', `" + date_field + "`)",
            'hours_of_day': "strftime('%%H', `" + date_field + "`)",
            'days_of_week': "strftime('%%w', `" + date_field + "`)",
            'months_of_year': "strftime('%%m', `" + date_field + "`)",
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
from django.db.models import Count, Sum
def time_series(qs, date_field, aggregate=None, interval='days', engine=None):
    aggregate = aggregate or Count('id')
    engine = engine or _guess_engine(qs)

    interval_sql = _get_interval_sql(date_field, interval, engine)
    aggregate_data = qs.extra(select = {'agg_date': interval_sql}).\
                            order_by().values('agg_date').\
                            annotate(agg=aggregate)

    return [(x['agg_date'], x['agg']) for x in aggregate_data]


from datetime import datetime
from bars_transactions.models import Transaction
def compute_transaction_stats(request, filter=id, aggregate=None):
    qs = Transaction.objects.filter(canceled=False)
    qs = filter(qs)

    if request.bar:
        qs = qs.filter(bar=request.bar)

    date_start = request.query_params.get('date_start')
    date_end = request.query_params.get('date_end', datetime.now())
    if date_start is not None:
        qs = qs.filter(timestamp__range=(date_start, date_end))

    types = request.query_params.getlist("type")
    if len(types) != 0:
        qs = qs.filter(type__in=types)

    qs = qs.order_by('-timestamp', '-id').distinct()

    interval = request.query_params.get('interval', 'days')
    result = time_series(qs, date_field='timestamp', interval=interval, aggregate=aggregate)
    return sorted(result)

from bars_core.models.account import Account
def compute_total_spent(request, filter=id, aggregate=None):
    qs = Transaction.objects.filter(canceled=False)
    qs = filter(qs)

    if request.bar:
        qs = qs.filter(bar=request.bar)

    date_start = request.query_params.get('date_start')
    date_end = request.query_params.get('date_end', datetime.now())
    if date_start is not None:
        qs = qs.filter(timestamp__range=(date_start, date_end))

    types = request.query_params.getlist("type")
    if len(types) != 0:
        qs = qs.filter(type__in=types)

    result = qs.aggregate(total_spent = Sum('accountoperation__delta'))
    return result

def compute_account_ranking(request):
    bar = request.query_params.get('bar')
    if bar is None:
        return None

    qs = Account.objects.filter(bar=bar).exclude(owner__username="bar").filter(deleted=False)
    t_filter = {'accountoperation__transaction__canceled': False}

    date_start = request.query_params.get('date_start')
    date_end = request.query_params.get('date_end', datetime.now())
    if date_start is not None:
        t_filter['accountoperation__transaction__timestamp__range'] = (date_start, date_end)

    types = request.query_params.getlist("type")
    if len(types) != 0:
        t_filter['accountoperation__transaction__type__in'] = types

    qs = qs.filter(**t_filter)

    result = qs.values('id').annotate(total_spent=Sum('accountoperation__delta'))
    return result

from bars_items.models.sellitem import SellItem
from django.db.models import F
def compute_sellitem_ranking(request, pk=None):
    if request.bar is None:
        return None
    else:
        bar = request.bar

    qs = Account.objects.filter(bar=bar)
    qs = qs.exclude(owner__username="bar").filter(deleted=False)

    t_filter = {'accountoperation__transaction__canceled': False, 'accountoperation__transaction__itemoperation__target__sellitem': pk}

    date_start = request.query_params.get('date_start')
    date_end = request.query_params.get('date_end', datetime.now())
    if date_start is not None:
        t_filter['accountoperation__transaction__timestamp__range'] = (date_start, date_end)

    t_filter['accountoperation__transaction__type__in'] = ("buy", "meal")

    qs = qs.filter(**t_filter)

    result = qs.values('id').annotate(total_spent=Sum(F('accountoperation__transaction__itemoperation__delta') * F('accountoperation__transaction__itemoperation__target__unit_factor')))
    return result

    
def compute_sellitem_by_account_ranking(request, pk=None):
    if request.bar is None:
        return None
    else:
        bar = request.bar

    qs = SellItem.objects.filter(bar=bar, deleted=False)

    t_filter = {'stockitems__itemoperation__transaction__canceled': False, 'stockitems__itemoperation__transaction__accountoperation__target': pk}

    date_start = request.query_params.get('date_start')
    date_end = request.query_params.get('date_end', datetime.now())
    if date_start is not None:
        t_filter['stockitems__itemoperation__transaction__timestamp__range'] = (date_start, date_end)

    t_filter['stockitems__itemoperation__transaction__type__in'] = ("buy", "meal")

    qs = qs.filter(**t_filter)

    result = qs.values('id', 'name').annotate(nb_transactions=Count('stockitems__itemoperation__transaction'))
    return result