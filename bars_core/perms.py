## View-related permissions; forwards to bar- or object-related permissions
from rest_framework.permissions import DjangoObjectPermissions
from restfw_composed_permissions.base import BasePermissionComponent, BaseComposedPermision, And
from restfw_composed_permissions.generic.components import AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod
from restfw_composed_permissions.generic.components import ObjectAttrEqualToObjectAttr as ObjectAttrEqualToObjectAttr_
from bars_django.utils import get_root_bar

DEBUG = False

# Fix library
class ObjectAttrEqualToObjectAttr(ObjectAttrEqualToObjectAttr_):
    def has_permission(self, perm_obj, request, view):
        return True

class BaseComposedPermission(BaseComposedPermision):
    def global_permission_set(self):
        return self.permission_set()

    def object_permission_set(self):
        return self.permission_set()


class PerBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, PerBarPermission) \
        | And(AllowOnlySafeHttpMethod, AllowAll)


class PerBarPermission(BasePermissionComponent, DjangoObjectPermissions):
    def get_required_permissions(self, method, view):
        model_cls = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_cls is None and queryset is not None:
            model_cls = queryset.model

        assert model_cls, ('Cannot apply permissions on a view that'
                           ' does not have `.model` or `.queryset` property.')

        return DjangoObjectPermissions.get_required_permissions(self, method, model_cls)

    def has_permission(self, perm_obj, request, view):
        bar = request.bar
        perms = self.get_required_permissions(request.method, view)
        if DEBUG:
            print "View: ", request.method, bar, perms
        return request.user.has_perms(perms, bar)

    def has_object_permission(self, perm_obj, request, view, obj):
        if DEBUG:
            print "View (obj): ", request.method, obj
        return DjangoObjectPermissions.has_object_permission(self, request, view, obj)


class RootBarPermissionsOrAnonReadOnly(BaseComposedPermission):
    permission_set = lambda self: \
        And(AllowOnlyAuthenticated, RootBarPermission) \
        | And(AllowOnlySafeHttpMethod, AllowAll)


class RootBarPermission(PerBarPermission):
    def has_permission(self, perm_obj, request, view):
        bar = get_root_bar()
        perms = self.get_required_permissions(request.method, view)
        if DEBUG:
            print "View (root): ", request.method, bar, perms
        return request.user.has_perms(perms, bar)



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
            print "Logic: ", perm, obj
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
            print "Logic: ", perm, obj
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
            print "Backend (%s): " % method, perm, repr(obj), res, list(reduce(lambda x, y:x | set(y), [r.get_permissions() for r in user.role_set.all()], set()))
        return res
