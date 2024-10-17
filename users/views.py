from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


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
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        posts = user.post_set.all()
        followers = user.followers.all()
        following = user.following.all()
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        
        return render(request, 'users/profile.html', {
            'user': user,
            'posts': posts,
            'followers': followers,  
            'following': following,  
            'is_following': is_following,
        })

class ProfileEdit(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        profile, created = Profile.objects.get_or_create(user=user)
        form = ProfileForm(instance=profile)
        
        return render(request, 'users/edit_profile.html', {
            'form': form,
            'user': user,
        })

    def post(self, request, id):
        user = get_object_or_404(User, id=id)

        if request.user != user:
            return redirect('profile_view', id=id)

        profile, created = Profile.objects.get_or_create(user=user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user  
            profile.save()  
            return redirect('profile_view', id=id)

        return render(request, 'users/edit_profile.html', {
            'form': form,
            'user': user,
        })

class FollowUser(View):
    def post(self, request, id):
        user_to_follow = get_object_or_404(User, id=id)
        if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
            Follow.objects.create(follower=request.user, following=user_to_follow)
            return redirect('profile_view', id=id)
        return redirect('profile_view', id=id)

class UnfollowUser(View):
    def post(self, request, id):
        user_to_unfollow = get_object_or_404(User, id=id)
        follow_record = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follow_record.exists():
            follow_record.delete()
        return redirect('profile_view', id=id)
