from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, UserListSerializer, UserListSerializerget

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

from rest_framework import permissions
from snippets.permissions import AllowOnlyAnonymous, AllowOnlyOwnProfile, AllowToEditOwnSnippets

from rest_framework.reverse import reverse
from rest_framework import renderers

from snippets.serializers import GlobalSearchSerializer

from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.views import APIView


class SnippetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_fields = ('language', 'code')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowToEditOwnSnippets,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserList(generics.ListCreateAPIView):
    permission_classes = (AllowOnlyAnonymous,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer = UserListSerializer
        if self.request.method == 'GET':
            serializer.Meta.fields = serializer.Meta.fields_GET
        else:
            serializer.Meta.fields = serializer.Meta.fields_POST
        return serializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (AllowOnlyOwnProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

from django.db.models import Q
from itertools import chain

class GlobalSearchList(generics.ListAPIView):
   serializer_class = GlobalSearchSerializer

   def get_queryset(self):
      query = self.request.query_params.get('id', None)
      return Snippet.objects.filter(owner__username=query)#all_results
