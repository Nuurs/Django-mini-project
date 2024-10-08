from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})

class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, 'blog/post_detail.html', {'post': post})

class PostCreate(APIView):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', id=post.id)
        return render(request, 'blog/post_form.html', {'form': form})

class PostEdit(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = PostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
        return render(request, 'blog/post_form.html', {'form': form})

class PostDelete(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, 'blog/post_confirm_delete.html', {'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect('post_list')

class AddComment(APIView):
    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=id)
        return render(request, 'blog/post_detail.html', {'post': post, 'form': form})
