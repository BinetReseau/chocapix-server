# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import Group
from django import forms

from bars_items.models.buyitem import BuyItem, BuyItemPrice
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.sellitem import SellItem
from bars_items.models.stockitem import StockItem
from bars_items.models.suggesteditem import SuggestedItem


class ItemDetailsAdmin(admin.ModelAdmin):
   list_display   = ('name', 'brand', 'container', 'unit')
   ordering       = ('name', 'brand', 'container', 'unit')
   search_fields  = ('name', 'keywords', 'buyitem__barcode', )
   exclude = None

admin.site.register(BuyItem)
admin.site.register(BuyItemPrice)
admin.site.register(ItemDetails, ItemDetailsAdmin)
admin.site.register(SellItem)
admin.site.register(StockItem)
admin.site.register(SuggestedItem)
