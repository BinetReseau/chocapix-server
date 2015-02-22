from django.contrib import admin
from bars_base.models.account import Account
from bars_base.models.item import Item, ItemDetails

admin.site.register(Account)
admin.site.register(Item)
admin.site.register(ItemDetails)
