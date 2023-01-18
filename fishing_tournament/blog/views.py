from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from . import data
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-date_posted']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['fish_type', 'fish_length', 'img']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['fish_type', 'fish_length', 'img']
    success_url = '/posts'
    template_name = 'blog/post_form_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def dashboard(request):
    context = {
        'ScoresList': [
            data.get_user_scores_koenigsklasse(request)[:3],
            data.get_user_scores_schleie(request)[:3],
            data.get_user_scores_karpfen(request)[:3]
        ]
    }
    return render(request, 'blog/dashboard.html', context)


@login_required
def koenigsklasse(request):
    context = {
        'UserScoresKoenigsklasse': data.get_user_scores_koenigsklasse(request)
    }
    return render(request, 'blog/koenigsklasse.html', context)


@login_required
def rotauge(request):
    context = {
        'UserScoresRotauge': data.get_user_scores_rotauge(request)
    }
    return render(request, 'blog/rotauge.html', context)


@login_required
def schleie(request):
    context = {
        'UserScoresSchleie': data.get_user_scores_schleie(request)
    }
    return render(request, 'blog/schleie.html', context)


@login_required
def karpfen(request):
    context = {
        'UserScoresKarpfen': data.get_user_scores_karpfen(request)
    }
    return render(request, 'blog/karpfen.html', context)


@login_required
def table(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'blog/table.html', context)


@login_required
def rules(request):
    return render(request, 'blog/rules.html')
