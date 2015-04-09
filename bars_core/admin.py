from django.contrib import admin
from django.contrib.auth.models import Group
from bars_core.models.user import User
from bars_core.models.bar import Bar, BarSettings
from bars_core.models.role import Role
from bars_core.models.account import Account
from bars_core.models.loginattempt import LoginAttempt


admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Bar)
admin.site.register(BarSettings)
admin.site.register(Role)
admin.site.register(Account)
admin.site.register(LoginAttempt)
