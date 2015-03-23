from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, _user_has_module_perms, _user_has_perm
from rest_framework import viewsets, serializers, decorators, exceptions
from rest_framework.response import Response
from permission.logics import OneselfPermissionLogic

from bars_django.utils import VirtualField, permission_logic
from bars_core.perms import RootBarRolePermissionLogic


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().prefetch_related('role_set')

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


@permission_logic(OneselfPermissionLogic())
@permission_logic(RootBarRolePermissionLogic())
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
        read_only_fields = ('is_active', 'last_login', 'last_modified')
        write_only_fields = ('password',)
        exclude = ('is_staff', 'is_superuser')
        extra_kwargs = {'password':{'required':False}}
    _type = VirtualField("User")

    def create(self, data):
        u = super(UserSerializer, self).create(data)
        u.set_password(data.get('password', '0000'))
        u.save()
        return u


from restfw_composed_permissions.generic.components import AllowOnlyAuthenticated
from bars_core.perms import BaseComposedPermission, RootBarPermission, ObjectAttrEqualToObjectAttr
class UserPermissions(BaseComposedPermission):
    permission_set = lambda self: \
        AllowOnlyAuthenticated() & (RootBarPermission() | ObjectAttrEqualToObjectAttr("request.user", "obj"))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

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

    @decorators.detail_route(methods=['put'])
    def reset_password(self, request, pk=None):
        user = User.objects.get(pk=pk)
        # password = User.objects.make_random_password()
        password = "0000"

        user.set_password(password)
        user.save()
        return Response('Password changed', 200)


def get_default_user():
    if get_default_user._cache is None:
        get_default_user._cache, _ = User.objects.get_or_create(username="bar", full_name="Bar", is_active=False)
    return get_default_user._cache
get_default_user._cache = None
