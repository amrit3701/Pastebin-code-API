from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

from rest_framework.reverse import reverse
from rest_framework import renderers

from snippets.serializers import GlobalSearchSerializer

class SnippetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)#OrReadOnly, IsOwnerOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_fields = ('language', 'code')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)#OrReadOnly, IsOwnerOrReadOnly,)

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
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
