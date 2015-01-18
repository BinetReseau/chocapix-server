from permission.utils.field_lookup import field_lookup
from permission.logics import PermissionLogic, AuthorPermissionLogic
from bars_api.models.role import Role

# For reference
perms_list = [
    'bars_api.create_buytransaction',
    'bars_api.create_throwtransaction',
    'bars_api.create_givetransaction',
    'bars_api.create_punishtransaction',
    'bars_api.create_mealtransaction',
    'bars_api.create_approtransaction',
    'bars_api.create_inventorytransaction',

    # 'bars_api.create_bar',
    # 'bars_api.create_user',
    'bars_api.create_role',
    'bars_api.create_account',
    'bars_api.create_item',
    # 'bars_api.create_transaction',
    'bars_api.create_news',

    # 'bars_api.change_bar',
    # 'bars_api.change_user',
    'bars_api.change_role',
    'bars_api.change_account',
    'bars_api.change_item',
    'bars_api.change_transaction',
    'bars_api.change_news',

    # 'bars_api.delete_bar',
    # 'bars_api.delete_user',
    'bars_api.delete_role',
    'bars_api.delete_account',
    'bars_api.delete_item',
    'bars_api.delete_transaction',
    'bars_api.delete_news',
]

# ## Per-bar permissions

class BarPermissionBackend(object):
    def has_perm(self, user, perm, bar=None):
        if not user.is_authenticated():
            return False

        if bar is None:
            return True
        elif user.is_active:
            roles = Role.objects.filter(user=user, bar=bar)
            for r in roles:
                if perm in r.get_permissions():
                    return True

        return False



# ## Per-object permissions

class BarRolePermissionLogic(PermissionLogic):
    def __init__(self, field_name=None):
        self.field_name = field_name or 'bar'

    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated():
            return False

        if obj is None:
            return True
        elif user.is_active:
            bar = field_lookup(obj, self.field_name)
            if bar is None:
                return False
            roles = Role.objects.filter(user=user, bar=bar)
            for r in roles:
                if perm in r.get_permissions():
                    return True
            return False


PERMISSION_LOGICS = (
    ('bars_api.Account', BarRolePermissionLogic()),
    ('bars_api.Item', BarRolePermissionLogic()),
    # ('bars_api.News', BarRolePermissionLogic()),
    ('bars_api.Role', BarRolePermissionLogic()),
    ('bars_api.Transaction', BarRolePermissionLogic()),
    ('bars_api.Transaction', AuthorPermissionLogic(field_name='author')),
)
