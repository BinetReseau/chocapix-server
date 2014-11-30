from bars_api.models.user import User, make_password


class AuthenticationBackend(object):
    def authenticate(self, password=None):
        if password is None:
            return None
        encoded_password = make_password(password)
        try:
            return User.objects.get(password=encoded_password)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    # def has_perm(self, user_obj, perm, obj=None):
