from rest_framework.permissions import DjangoObjectPermissions
from permission.utils.field_lookup import field_lookup
from permission.logics import PermissionLogic, OneselfPermissionLogic
from restfw_composed_permissions.base import BasePermissionComponent, BaseComposedPermision, And, Or
from restfw_composed_permissions.generic.components import AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod, ObjectAttrEqualToObjectAttr
from bars_core.models.bar import Bar



# View-related permissions; forwards to bar-related permissions
class PerBarPermissionsOrAnonReadOnly(BaseComposedPermision):
    def global_permission_set(self):
        return Or(And(AllowOnlyAuthenticated, PerBarPermission),
                  And(AllowOnlySafeHttpMethod, AllowAll))

    def object_permission_set(self):
        return Or(And(AllowOnlyAuthenticated, ObjectAttrEqualToObjectAttr("request.bar", "obj.bar"), PerBarPermission),
                  And(AllowOnlySafeHttpMethod, AllowAll))


class PerBarPermission(BasePermissionComponent, DjangoObjectPermissions):
    def has_permission(self, perm_obj, request, view):
        bar = request.bar
        if bar is not None:
            model_cls = getattr(view, 'model', None)
            queryset = getattr(view, 'queryset', None)

            if model_cls is None and queryset is not None:
                model_cls = queryset.model

            assert model_cls, ('Cannot apply permissions on a view that'
                               ' does not have `.model` or `.queryset` property.')

            perms = self.get_required_permissions(request.method, model_cls)

            # print "View: ", request.method, bar, perms
            return request.user.has_perms(perms, bar)

        return False


    def has_object_permission(self, perm_obj, request, view, obj):
        # print "View (obj): ", request.method, obj
        # Handled by BarRolePermissionLogic
        return DjangoObjectPermissions.has_object_permission(self, request, view, obj)


# Object-related permissions; forwards to bar-related permissions
class BarRolePermissionLogic(PermissionLogic):
    def __init__(self, field_name=None):
        self.field_name = field_name or 'bar'

    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        # print "Logic: ", perm, obj
        if obj is None:
            method = perm.split(".")[1].split("_")[0]
            return method in ('change', 'delete')
        else:
            bar = field_lookup(obj, self.field_name)
            return user.has_perm(perm, bar)

        return False



# Bar-related permissions
from permission.backends import PermissionBackend as PermissionBackend_
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

        if isinstance(obj, Bar):
            method = "bar"
            res = _has_perm_in_bar(user, perm, obj)
        else:
            method = "obj"
            res = super(PermissionBackend, self).has_perm(user, perm, obj)

        # print "Backend (%s): " % method, perm, repr(obj), res
        return res
