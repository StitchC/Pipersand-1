from game.models import Profile, Record

from django.shortcuts import render
from django.utils import timezone
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed,
    HttpResponseBadRequest)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

import jsonpickle

# import sys
# sys.path.append("C:/Users/67089/Documents/GitHub/Pipersand")
from Sandbox.core.Company import Company



@ensure_csrf_cookie
def set_cookie(request):
    return HttpResponse("welcome")


def create_user(request):
    """
    ./register POST
    username: 用户名
    password: 密码
    email: 邮箱
    """
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(username, email, password)
    profile = Profile(user=user)
    profile.save()
    return HttpResponse("创建新用户成功")


def login(request):
    """
    ./login POST
    username: 用户名
    password: 密码
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username,password=password)
    if user is not None:
        auth_login(request, user)
        # Redirect to a success page.
        return HttpResponse("login successed")
    else:
        return HttpResponseRedirect('/home')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/home')


@login_required
def changing_password(request):
    """
    ./modify_password POST
    new_password: 新密码
    """
    new_password = request.POST['new_password']
    u = request.user
    u.set_password(new_password)
    u.save()
    return HttpResponse('ok')


@login_required
def start_game(request):
    """
    # 创建或者加入了公司的玩家可以选择一个房间点开始游戏
    # ./game/start_game POST
    # room_id: 房间号

    点开始游戏，创建一个Company object，存到数据库里面
    """
    c = Company()
    user = get_user(request)
    profile = user.Profile

    record = Record(status=jsonpickle.dumps(c),
                    time=timezone.now(),
                    player=user)
    record.save()

    profile.current_game = record
    profile.save()

    return HttpResponse('ok')
