from datetime import timedelta
from django.utils import timezone
from permission.logics import AuthorPermissionLogic
from bars_core.perms import debug_perm

class TransactionAuthorPermissionLogic(AuthorPermissionLogic):
    @debug_perm("Logic (transaction)")
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        if obj is not None and perm == 'bars_transactions.change_transaction':
            threshold = obj.bar.settings.transaction_cancel_threshold
            if timezone.now() - obj.timestamp > timedelta(hours=threshold):
                return False

        return super(TransactionAuthorPermissionLogic, self).has_perm(user, perm, obj)
