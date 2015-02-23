from django.contrib import admin
from bars_items.models.buyitem import BuyItem, BuyItemPrice
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.sellitem import SellItem
from bars_items.models.stockitem import StockItem

admin.site.register(BuyItem)
admin.site.register(BuyItemPrice)
admin.site.register(ItemDetails)
admin.site.register(SellItem)
admin.site.register(StockItem)
