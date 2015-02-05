from bars_core.perms import BarRolePermissionLogic

PERMISSION_LOGICS = (
    ('bars_api.Account', BarRolePermissionLogic()),
    ('bars_api.Item', BarRolePermissionLogic()),
)
