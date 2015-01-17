from permission.logics import AuthorPermissionLogic

PERMISSION_LOGICS = (
    ('bars_api.Transaction', AuthorPermissionLogic(field_name='author')),
)
