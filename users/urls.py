from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='user_login'),         
    path('logout/', views.UserLogout.as_view(), name='user_logout'), 
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile_view'),  # Changed to <int:id>
    path('profile/<int:id>/edit/', views.ProfileEdit.as_view(), name='profile_edit'),
    path('follow/<int:id>/', views.FollowUser.as_view(), name='follow_user'),  # Changed to <int:id>
    path('unfollow/<int:id>/', views.UnfollowUser.as_view(), name='unfollow_user'),  # Changed to <int:id>
]
