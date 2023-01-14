from rest_framework.permissions import BasePermission


class UserAdminOrOwner(BasePermission):
    """
    Object-level permission to allow owners of an object to see and edit it.
    Allow Admin and staff to see and edit their own and
    others beneath them objects.
    """

    def has_object_permission(self, request, view, user):
        if (
            self.__has_no_permission_to_update_superuser_details(request, user)
            or self.__has_no_permission_to_update_staff_details(request, user)
            or self.__has_no_permission_to_update_other_user_details(
                request, user)
        ):
            return False
        return True

    def __has_no_permission_to_update_superuser_details(self, request, user):
        if (
            request.user.is_superuser
            and user.is_superuser
            and request.user.id != user.id
        ):
            return True

    def __has_no_permission_to_update_staff_details(self, request, user):
        if (
            not request.user.is_superuser
            and request.user.is_staff
            and (user.is_staff or user.is_superuser)
            and request.user.id != user.id
        ):
            return True

    def __has_no_permission_to_update_other_user_details(self, request, user):
        if (
            not request.user.is_superuser
            and not request.user.is_staff
            and request.user.id != user.id
        ):
            return True
