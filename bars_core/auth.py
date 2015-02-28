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
from bars_django.utils import get_client_ip
from bars_core.models.loginattempt import LoginAttempt
class ObtainJSONWebTokenWrapper(ObtainJSONWebToken):
    def post(self, request):
        response = super(ObtainJSONWebTokenWrapper, self).post(request)

        ip = get_client_ip(request)
        success = response.status_code != 400
        sent_username=request.data.get('username')
        try:
            user = User.objects.get(username=sent_username)
        except User.DoesNotExist:
            user = None
        LoginAttempt.objects.create(user=user, success=success, ip=ip, sent_username=sent_username)

        return response

obtain_jwt_token = ObtainJSONWebTokenWrapper.as_view()
