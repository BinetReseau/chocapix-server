from permission.logics import AuthorPermissionLogic
from bars_core.perms import BarRolePermissionLogic

PERMISSION_LOGICS = (
    ('bars_api.Transaction', BarRolePermissionLogic()),
    ('bars_api.Transaction', AuthorPermissionLogic(field_name='author')),
)
