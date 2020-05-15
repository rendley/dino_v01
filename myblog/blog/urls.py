from django.urls import path

from .views import *


urlpatterns = [

    path('', PostListView.as_view(), name='post_list'),
    path('create/', post_create, name='post_create'),
    path('<int:pk>/share/', post_share, name='post_share'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    # path('<int:pk>/', PostDetailView.as_view(), name='post_detail')
]