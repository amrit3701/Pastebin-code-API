from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.models import Snippet

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

class AllowToEditOwnSnippets(permissions.BasePermission):
    """
    Allow only user edit only his/her Snippet.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_anonymous and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_authenticated:
            snippet = Snippet.objects.get(id=view.kwargs['pk'])
            if snippet.owner == request.user:
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
        else:
            return False
