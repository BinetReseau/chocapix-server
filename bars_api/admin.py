from django.contrib import admin
from django.contrib.auth.models import Group

from bars_api.models import *
from bars_api.models.bar import Bar
from bars_api.models.user import User
from bars_api.models.account import Account
from bars_api.models.role import Role
from bars_api.models.item import Item
from bars_api.models.news import News
from bars_api.models.transaction import Transaction

admin.site.register(Bar)
admin.site.register(Account)
admin.site.register(Role)
admin.site.register(Item)
admin.site.register(News)
admin.site.register(Transaction)
# admin.site.register(AccountOperation)
# admin.site.register(ItemOperation)

admin.site.register(User)
admin.site.unregister(Group)
