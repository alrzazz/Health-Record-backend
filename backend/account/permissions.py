from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to manager.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 0)


class IsPatient(BasePermission):
    """
    Allows access only to Petients.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 2)


class IsDoctor(BasePermission):
    """
    Allows access only to Doctors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 1)


class NotManager(BasePermission):
    """
    Allows access to patients and doctors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.role == 0)
