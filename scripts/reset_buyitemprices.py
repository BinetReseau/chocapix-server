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
            try:
                bip.price = bip.buyitem.details.stockitems[0].price * bip.buyitem.itemqty
                bip.save()
            except IndexError:
                print("ERROR !")
                print("Bar : %s" % bar)
                print("Aliment : %s" % bip.buyitem.details.name)
                print("BuyItemPrice : %d" % bip.id)
                print("BuyItem : %d" % bip.buyitem.id)
                print("ItemDetails : %d" % bip.buyitem.details.id)
