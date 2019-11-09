from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm
from .models import Profile
from django.views.generic import (
    ListView, 
    DetailView, 
    UpdateView
)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, '{} hat sich am Fishing Tournament angemeldet. Petri Heil!'.format(username))
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


class ProfileListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/profiles.html'
    context_object_name = 'users'
    ordering = ['-date_joined']


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'user_profile'


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email'] 
    success_url = '/profiles'
    template_name = 'users/profile_form_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        user_profile = self.get_object()
        if self.request.user.id == user_profile.id:
            return True
        return False


class ProfileImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['image'] 
    success_url = '/profiles'
    template_name = 'users/profile_img_form_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        user_profile = self.get_object()
        if self.request.user.id == user_profile.id:
            return True
        return False
