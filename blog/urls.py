from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),  # Updated to use PostList class
    path('post/<int:id>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostCreate.as_view(), name='post_create'),
    path('post/edit/<int:id>/', views.PostEdit.as_view(), name='post_edit'),
    path('post/delete/<int:id>/', views.PostDelete.as_view(), name='post_delete'),
]
