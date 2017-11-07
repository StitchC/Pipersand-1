"""Pipersand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from game import views as game_views
from common import views as common_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_token/', common_views.set_cookie),
    url(r'^register', common_views.create_user),
    url(r'^login', common_views.login),
    url(r'^logout', common_views.logout),
    url(r'^modify_password', common_views.changing_password),
    url(r'^start_game', common_views.start_game),
    url(r'^game/', include('game.urls')),
]
