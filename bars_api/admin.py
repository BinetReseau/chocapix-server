from django.contrib import admin
from django.contrib.auth.models import Group

from bars_api.models import *
from bars_api.auth import User

admin.site.register(Bar)
admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(AccountOperation)
admin.site.register(ItemOperation)

admin.site.register(User)
admin.site.unregister(Group)
