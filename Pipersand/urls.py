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
from django.conf.urls import url
from django.contrib import admin
from game import views as game_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_token/', game_views.set_cookie),
    url(r'^game/create_company', game_views.create_company),
    url(r'^game/join_company', game_views.join_company),
    url(r'^register', game_views.create_user),
    url(r'^login', game_views.login),
    url(r'^logout', game_views.logout),
    url(r'^start_game', game_views.start_game),
    url(r'^game/(\w+)$', game_views.cmd_proxy),
    url(r'^game/util/roll_back', game_views.roll_back),
    url(r'^game/long_loan', game_views.long_loan),
    url(r'^test/(\d+)', game_views.test_param),
]
