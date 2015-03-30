from rest_framework.permissions import DjangoObjectPermissions
from restfw_composed_permissions.base import BasePermissionComponent, BaseComposedPermision, And, Or
from restfw_composed_permissions.generic.components import AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod
from bars_django.utils import get_root_bar

DEBUG = False


class BaseComposedPermission(BaseComposedPermision):
    def global_permission_set(self):
        return self.permission_set()

    def object_permission_set(self):
        return self.permission_set()


class DjangoObjectPermissionComponent(BasePermissionComponent, DjangoObjectPermissions):
    def has_permission(self, perm_obj, request, view):
        if DEBUG:
            print("View: ", request.method)
        return DjangoObjectPermissions.has_permission(self, request, view)

    def has_object_permission(self, perm_obj, request, view, obj):
        if DEBUG:
            print("View (obj): ", request.method, obj)
        return DjangoObjectPermissions.has_object_permission(self, request, view, obj)



## View-related permissions; forwards to bar- or object-related permissions
class PerBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, PerBarPermissionComponent) \
        | And(AllowOnlySafeHttpMethod, AllowAll)

class PerBarPermissionsOrAuthedReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, Or(PerBarPermissionComponent, AllowOnlySafeHttpMethod))

class PerBarPermissions(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, PerBarPermissionComponent)

class PerBarPermissionComponent(DjangoObjectPermissionComponent):
    def has_permission(self, perm_obj, request, view):
        bar = request.bar
        return self.has_object_permission(perm_obj, request, view, bar)


class RootBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, RootBarPermissionComponent) \
        | And(AllowOnlySafeHttpMethod, AllowAll)


class RootBarPermissionComponent(DjangoObjectPermissionComponent):
    def has_permission(self, perm_obj, request, view):
        bar = get_root_bar()
        return self.has_object_permission(perm_obj, request, view, bar)



## Object-related permissions; forwards to bar-related permissions
from permission.utils.field_lookup import field_lookup
from permission.logics import PermissionLogic
class BarRolePermissionLogic(PermissionLogic):
    def __init__(self, field_name=None):
        self.field_name = field_name or 'bar'

    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        if DEBUG:
            print("Logic: ", perm, obj)
        if obj is None:
            method = perm.split(".")[1].split("_")[0]
            return method in ('change', 'delete')
        else:
            bar = field_lookup(obj, self.field_name)
            return user.has_perm(perm, bar)

        return False


class RootBarRolePermissionLogic(PermissionLogic):
    def __init__(self, field_name=None):
        self.field_name = field_name or 'bar'

    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        if DEBUG:
            print("Logic: ", perm, obj)
        bar = get_root_bar()
        return user.has_perm(perm, bar)



## Bar-related permissions
from permission.backends import PermissionBackend as PermissionBackend_
from bars_core.models.bar import Bar

def _has_perm_in_bar(user, perm, bar):
    for r in user.role_set.all():
        if r.bar_id == bar.id and perm in r.get_permissions():
            return True
    return False

class PermissionBackend(PermissionBackend_):
    def authenticate(self, *args, **kwargs):
        return None

    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        bar_perm = "bar" == perm.split(".")[1].split("_")[1]
        if isinstance(obj, Bar) and (obj == get_root_bar() or not bar_perm):
            method = "bar"
            res = _has_perm_in_bar(user, perm, obj)
        else:
            method = "obj"
            res = super(PermissionBackend, self).has_perm(user, perm, obj)

        if DEBUG:
            print("Backend (%s): " % method, perm, repr(obj), res, list(reduce(lambda x, y:x | set(y), [r.get_permissions() for r in user.role_set.all()], set())))
        return res
