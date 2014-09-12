from django.contrib import admin

from bars_api.models import *

admin.site.register(User)
admin.site.register(Bar)
admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(AccountOperation)
admin.site.register(ItemOperation)
