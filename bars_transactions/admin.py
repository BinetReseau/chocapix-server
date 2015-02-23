from django.contrib import admin
from bars_transactions.models import Transaction, AccountOperation, ItemOperation

admin.site.register(Transaction)
admin.site.register(AccountOperation)
admin.site.register(ItemOperation)
