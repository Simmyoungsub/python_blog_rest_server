from django.conf.urls import url
from django.contrib import admin
from blog.views import *

urlpatterns = [
    url(r'^user/$', Users.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$',UserDetail.as_view()),
    url(r'^sign/signin/$',UserSign.as_view()),
    url(r'^sign/signout/$',UserSignout.as_view()),
    url(r'^sign/refresh/$',TokenRefresh.as_view()),
    url(r'^test/$',Test.as_view()),
    url(r'^board/$',BoardView.as_view()),
    url(r'^board/(?P<pk>[0-9]+)/$',BoardDetailView.as_view())
]
