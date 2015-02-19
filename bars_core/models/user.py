from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, _user_has_module_perms, _user_has_perm
from rest_framework import viewsets, serializers, decorators, exceptions
from rest_framework.response import Response

from bars_django.utils import VirtualField


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        app_label = 'bars_core'
    username = models.CharField(max_length=128, unique=True)
    full_name = models.CharField(max_length=128, blank=True)
    pseudo = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    # email = ''

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.full_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', '_type', 'username', 'full_name', 'pseudo', 'last_login', 'last_modified')
        read_only_fields = ('id', '_type', 'full_name', 'last_login', 'last_modified')
    _type = VirtualField("User")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.list_route()
    def me(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @decorators.list_route(methods=['put'])
    def change_password(self, request):
        user = request.user

        data = request.data
        if not user.check_password(data['old_password']):
            raise exceptions.PermissionDenied()

        user.set_password(data['password'])
        user.save()
        return Response('Password changed', 200)


def get_default_user():
    try:
        return User.objects.get(username="bar")
    except User.DoesNotExist:
        return User.objects.create(username="bar", full_name="Bar", is_active=False)
