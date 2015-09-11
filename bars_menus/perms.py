from permission.logics import AuthorPermissionLogic

class MenuOwnerPermissionLogic(AuthorPermissionLogic):
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        # if obj is not None and perm in ('bars_menus.change_menu', 'bars_menus.delete_menu'):
        #     pass

        return super(MenuOwnerPermissionLogic, self).has_perm(user, perm, obj)
