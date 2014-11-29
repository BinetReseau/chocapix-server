from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from rest_framework import viewsets, serializers, decorators

from bars_api import VirtualField

import hashlib
def make_password(password):
    return hashlib.sha512(password).hexdigest()



class UserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# User
class User(models.Model):  # cannot inherit from AbstractBaseUser, need to override password field
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128, unique=True)
    full_name = models.CharField(max_length=128, blank=True)
    pseudo = models.CharField(max_length=128, blank=True)

    last_login = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    is_active = True


    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def __unicode__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password == make_password(raw_password)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password("")

    def has_usable_password(self):
        return self.password == make_password("")


    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.full_name


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return True



class AuthenticationBackend(object):
    def authenticate(self, password=None):
        if password is None: return None
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', '_type', 'username', 'full_name', 'pseudo', 'last_login', 'last_modified', 'password')
        write_only_fields = ('password',)
    _type = VirtualField("User")

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if 'password' in attrs:
            user.set_password(attrs['password'])
        return user


from rest_framework.response import Response
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.list_route()
    def me(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
