from datetime import timedelta
from django.utils import timezone
from permission.logics import AuthorPermissionLogic

class TransactionAuthorPermissionLogic(AuthorPermissionLogic):
    def has_perm(self, user, perm, obj=None):
        if not user.is_authenticated() or not user.is_active:
            return False

        if obj is not None and perm == 'bars_transactions.change_transaction':
            threshold = obj.bar.transaction_cancel_threshold
            # now = timezone.make_naive(timezone.now(), timezone.utc)
            if timezone.now() - obj.timestamp > timedelta(hours=threshold):
                return False

        return super(TransactionAuthorPermissionLogic, self).has_perm(user, perm, obj)
