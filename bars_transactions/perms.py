from permission.logics import AuthorPermissionLogic
from bars_core.perms import BarRolePermissionLogic

PERMISSION_LOGICS = (
    ('bars_transactions.Transaction', BarRolePermissionLogic()),
    ('bars_transactions.Transaction', AuthorPermissionLogic(field_name='author')),
)
