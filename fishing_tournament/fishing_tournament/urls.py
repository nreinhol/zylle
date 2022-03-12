"""fishing_tournament URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from blog.views import (
    rules,
    table,
    dashboard,
    koenigsklasse,
    rotauge,
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

from users.views import (
    register,
    ProfileListView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileImageUpdateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/<int:pk>/update_img', ProfileImageUpdateView.as_view(), name='profile-update-img'),
    path('dashboard/', dashboard, name='dashboard'),
    path('koenigsklasse/', koenigsklasse, name='koenigsklasse'),
    path('rotauge/', rotauge, name='rotauge'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('table/', table, name='table'),
    path('rules/', rules, name='rules'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    