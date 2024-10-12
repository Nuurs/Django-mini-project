from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Post
from .forms import PostForm, CommentForm

class PostList(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})

class PostDetail(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        comments = post.comments.all()  # Предполагается, что у вас есть связь комментариев с постами
        form = CommentForm()  # Форма для добавления комментария
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', id=post.id)
        return render(request, 'blog/post_form.html', {'form': form})

class PostEdit(View):
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

class PostDelete(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, 'blog/post_confirm_delete.html', {'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect('post_list')

class AddComment(View):
    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=id)
        comments = post.comments.all()  # Получаем все комментарии для отображения
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
