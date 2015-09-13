from rest_framework.permissions import DjangoObjectPermissions
from restfw_composed_permissions.base import BasePermissionComponent, BaseComposedPermision, And, Or
from restfw_composed_permissions.generic.components import AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod
from bars_django.utils import get_root_bar

DEBUG = False
DEBUG_INDENT = 0

def debug_begin(name, perm, obj):
    if DEBUG:
        global DEBUG_INDENT
        print("%s%s: %s, %s" % (" "*DEBUG_INDENT, name, perm, repr(obj)))
        DEBUG_INDENT += 1

def debug_end(name, perm, obj, res):
    if DEBUG:
        global DEBUG_INDENT
        DEBUG_INDENT -= 1
        print("%s%s: %s, %s => %s" % (" "*DEBUG_INDENT, name, perm, repr(obj), res))

def debug_perm(name):
    def wrapper(f):
        def f_(self, user, perm, obj=None):
            debug_begin(name, perm, obj)
            ret = f(self, user, perm, obj)
            debug_end(name, perm, obj, ret)
            return ret
        return f_
    return wrapper


class BaseComposedPermission(BaseComposedPermision):
    def global_permission_set(self):
        return self.permission_set()

    def object_permission_set(self):
        return self.permission_set()


class DjangoObjectPermissionComponent(BasePermissionComponent, DjangoObjectPermissions):
    def has_permission(self, perm_obj, request, view):
        debug_begin("View", request.method, None)
        res = DjangoObjectPermissions.has_permission(self, request, view)
        debug_end("View", request.method, None, res)

        return res

    def has_object_permission(self, perm_obj, request, view, obj):
        debug_begin("View (obj)", request.method, obj)
        res = DjangoObjectPermissions.has_object_permission(self, request, view, obj)
        debug_end("View (obj)", request.method, obj, res)

        return res



## View-related permissions; forwards to bar- or object-related permissions
class PerBarPermissions(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, PerBarPermissionComponent)

class PerBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, PerBarPermissionComponent) \
        | And(AllowOnlySafeHttpMethod, AllowAll)

class PerBarPermissionsOrAuthedReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, Or(PerBarPermissionComponent, AllowOnlySafeHttpMethod))

class PerBarPermissionsOrObjectPermissions(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, Or(PerBarPermissionComponent, DjangoObjectPermissionComponent))

class PerBarPermissionsOrObjectPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, Or(PerBarPermissionComponent, DjangoObjectPermissionComponent)) \
        | And(AllowOnlySafeHttpMethod, AllowAll)


class RootBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, RootBarPermissionComponent) \
        | And(AllowOnlySafeHttpMethod, AllowAll)

class RootBarPermissionsOrObjectPermissions(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, Or(RootBarPermissionComponent, DjangoObjectPermissionComponent))


class PerBarPermissionComponent(DjangoObjectPermissionComponent):
    def has_permission(self, perm_obj, request, view):
        bar = request.bar
        return self.has_object_permission(perm_obj, request, view, bar)

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

    @debug_perm("Logic")
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        if obj is None:
            method = perm.split(".")[1].split("_")[0]
            return method in ('change', 'delete')
        else:
            bar = field_lookup(obj, self.field_name)
            return user.has_perm(perm, bar)



class RootBarRolePermissionLogic(PermissionLogic):
    def __init__(self, field_name=None):
        self.field_name = field_name or 'bar'

    @debug_perm("Logic (root)")
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

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

    @debug_perm("Backend")
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        bar_perm = "bar" == perm.split(".")[1].split("_")[1]
        if isinstance(obj, Bar) and (obj == get_root_bar() or not bar_perm):
            return _has_perm_in_bar(user, perm, obj)
        else:
            return super(PermissionBackend, self).has_perm(user, perm, obj)
