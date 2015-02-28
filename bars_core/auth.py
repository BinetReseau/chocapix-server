from bars_core.models.user import User

class AuthenticationBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

from rest_framework_jwt.views import ObtainJSONWebToken
# from bars_django.utils import get_client_ip
class ObtainJSONWebTokenWrapper(ObtainJSONWebToken):
    def post(self, request):
        response = super(ObtainJSONWebTokenWrapper, self).post(request)
        # print get_client_ip(request)
        return response

obtain_jwt_token = ObtainJSONWebTokenWrapper.as_view()
