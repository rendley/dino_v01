from django.urls import path

from .views import *


urlpatterns = [

    path('', PostListView.as_view(), name="post_list_url"),
    path('<slug:slug>/', post_detail, name='post_detail_url')
]