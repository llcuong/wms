from rest_framework.permissions import BasePermission

class HasRBACPermission(BasePermission):
    app_code = None
    page_code = None
    permission_code = None

    def has_permission(self, request, view):
        user = request.user  # UserCustomUsers

        if not user or not user.is_authenticated:
            return False

        account = user.user_account
        if not account:
            return False

        return account.has_permission(
            self.app_code,
            self.page_code,
            self.permission_code
        )


class CanViewUser(HasRBACPermission):
    app_code = "USER"
    page_code = "USER_LIST"
    permission_code = "USER_VIEW"

