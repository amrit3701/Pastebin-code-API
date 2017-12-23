from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

#from rest_framework import routers
#router = routers.DefaultRouter()
#router.register(r'', views.UserList, 'list')

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="user-detail"),# views.Userdata.as_view({"get": "retrieve", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"})
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    url(r'^search/$', views.GlobalSearchList.as_view(), name="search"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
