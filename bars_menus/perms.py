from permission.logics import AuthorPermissionLogic

class MenuOwnerPermissionLogic(AuthorPermissionLogic):
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        return super(MenuOwnerPermissionLogic, self).has_perm(user, perm, obj)
