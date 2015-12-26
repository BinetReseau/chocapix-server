from django.db.models import Prefetch

from bars_core.models.bar import Bar
from bars_items.models.stockitem import StockItem
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.buyitem import BuyItem, BuyItemPrice

def run():
    for bar in Bar.objects.all():
        bips = BuyItemPrice.objects.filter(bar=bar).\
            select_related('buyitem', 'buyitem__details').\
            prefetch_related(Prefetch('buyitem__details__stockitem_set', queryset=StockItem.objects.filter(bar=bar), to_attr='stockitems'))
        for bip in list(bips):
            print(bip.price)
            bip.price = bip.buyitem.details.stockitems[0].price * bip.buyitem.itemqty
            print(bip.price)
            print("")
            bip.save()
