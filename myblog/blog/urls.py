from django.urls import path

from .views import *


urlpatterns = [

    path('', PostListView.as_view(), name='post_list'),
    path('login/', BlogLoginView.as_view(), name='login_page'),
    path('logout/', BlogLogoutView.as_view(), name='logout_page'),
    path('register/', BlogRegisterView.as_view(), name='register_page'),
    path('create/', post_create, name='post_create'),
    path('update/<int:pk>', post_update, name='post_update'),
    path('delete/<int:pk>', post_delete, name='post_delete'),
    path('create/comment/<int:pk>', comment_create, name='comment_create'),
    path('update/comment/<int:pk>', comment_update, name='comment_update'),
    path('<int:pk>/share/', post_share, name='post_share'),

    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    # path('<int:pk>/', PostDetailView.as_view(), name='post_detail')
]