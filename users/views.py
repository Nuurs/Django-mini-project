# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from rest_framework.views import APIView
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from rest_framework.response import Response
from django.utils.decorators import method_decorator

class UserLogin(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  
        return render(request, 'users/login.html', {'form': form})
class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('user_login') 
class UserRegistration(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        return render(request, 'users/registration.html', {'form': form})
class ProfileView(View):
    def get(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        posts = user.post_set.all()

       
        followers = [follow.follower for follow in user.followers.all()]
        following = [follow.following for follow in user.following.all()]
        
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

        return render(request, 'users/profile.html', {
            'user': user,
            'posts': posts,
            'followers': followers,  
            'following': following,  
            'is_following': is_following,
        })

class ProfileEdit(APIView):
    def get(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        return render(request, 'users/edit_profile.html', {
            'user': user,
        })

    def post(self, request, id, format=None):
        user = get_object_or_404(User, id=id)

        if request.user != user:
            return redirect('profile_view', id=id)


        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        if hasattr(user, 'profile'):
            user.profile.bio = bio
            if profile_picture:
                user.profile.profile_picture = profile_picture
            user.profile.save()
        else:
            Profile.objects.create(user=user, bio=bio, profile_picture=profile_picture)

        return redirect('profile_view', id=id)  



@method_decorator(login_required, name='dispatch')
class FollowUser(APIView):
    def post(self, request, id):
        user_to_follow = get_object_or_404(User, id=id)
        if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
            Follow.objects.create(follower=request.user, following=user_to_follow)
            return Response({"message": "Successfully followed."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already following."}, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(login_required, name='dispatch')
class UnfollowUser(APIView):
    def post(self, request, id):
        user_to_unfollow = get_object_or_404(User, id=id)
        follow_record = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follow_record.exists():
            follow_record.delete()
            return Response({"message": "Successfully unfollowed."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Not following this user."}, status=status.HTTP_400_BAD_REQUEST)