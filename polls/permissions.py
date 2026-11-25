
from rest_framework.permissions import BasePermission
from accounts.models import Profile

def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    if user.is_staff or user.is_superuser:
        return "ADMIN"

    try:
        return user.profile.role
    except Profile.DoesNotExist:
        return None


class IsPollCreatorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in ["ADMIN", "CREATOR"]

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        return (
            role == "ADMIN"
            or (
                role == "CREATOR"
                and obj.creator_id == request.user.id
            )
        )


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "PARTICIPANT"
