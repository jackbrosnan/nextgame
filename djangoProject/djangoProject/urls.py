"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin, auth
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.static import serve
from NextGame import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name="home"),
    path('home/', v.home, name="home"),
    path('register/', v.register, name="register"),
    path('profile/', v.profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    path('search/', v.search_title, name="search_title"),
    path('search_genre/<genre>/', v.search_genre, name="search-genre"),
    path('lookup/', v.search, name="lookup"),
    path('view/', v.view),
    path('liked_games/', v.liked_games, name="liked-games"),
    path('delete_liked_game/<id>', v.delete_liked_game, name="delete-game"),
    path('recommendations', v.recommendations, name="recommendations"),
    path('', include("django.contrib.auth.urls")),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)