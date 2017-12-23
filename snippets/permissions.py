from django.contrib.auth.models import User
from rest_framework import permissions

class AllowOnlyAnonymous(permissions.BasePermission):
    """
    Allow only anonymous user to POST.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        else:
            return request.method in permissions.SAFE_METHODS

class AllowOnlyOwnProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs['pk'])  #get user from user table.
        if request.user == user:
            return True
        else:
            return False
