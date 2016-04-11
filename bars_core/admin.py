from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import Group
from django import forms

from bars_core.models.user import User
from bars_core.models.bar import Bar, BarSettings
from bars_core.models.role import Role
from bars_core.models.account import Account
from bars_core.models.loginattempt import LoginAttempt

class BarForm(ActionForm):
    bar = forms.ModelChoiceField(queryset=Bar.objects.all())

class UserAdmin(admin.ModelAdmin):
    list_display   = ('pseudo', 'username', 'firstname')
    list_filter    = ('account__bar',)
    ordering       = ('pseudo', )
    search_fields  = ('username', 'firstname')
    exclude = None
    actions = ['admin']
    action_form = BarForm
   
    def admin(self, request, queryset):
        print([p for p in queryset])
        for user in queryset:
            print request.GET
            bar = request.POST.get('bar')
            print bar
            print user.account_set.all()[0].bar.id
            print Bar.objects.get(id=bar)
            Role.objects.create(name="admin", bar=Bar.objects.get(id=bar), user=user)
            Role.objects.create(name="staff", bar=Bar.objects.get(id="root"), user=user)
        
    admin.short_description = "Donner les droits de respo bar"


class RoleAdmin(admin.ModelAdmin):
   list_display   = ('user', 'bar', 'name')
   ordering       = ('bar', 'user', 'name')
   search_fields  = ('user__username', 'user__firstname' )
   exclude = None

"""class UserAdmin(admin.ModelAdmin):
   list_display   = ('pseudo', 'username', 'firstname')
   ordering       = ('pseudo', )
   search_fields  = ('username', 'firstname')
   exclude = None"""

admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
admin.site.register(Bar)
admin.site.register(BarSettings)
admin.site.register(Role, RoleAdmin)
admin.site.register(Account)
admin.site.register(LoginAttempt)
