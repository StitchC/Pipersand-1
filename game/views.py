from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed

from django.contrib.auth import authenticate, get_user
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from game.models import Company as Company_model, User, Record, Profile
from game.forms import long_loanForm
# Create your views here.

import sys
sys.path.append("C:/Users/67089/Documents/GitHub/Pipersand")
from Sandbox.core.Company import Company

import json
import jsonpickle
from datetime import datetime

# 每次开始游戏，对会在字典里面创建一个key为company_id的Company object
# game_obj = {}

def home(request):
    return HttpResponse("welcome")

def create_user(request):
    """
    ./game/register POST
    name: 用户名
    password: 密码
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
def create_company(request):
    """
    一个用户创建一个company，加入到company list里面
    ./game/create_company POST
    company_name: 公司名
    """
    company_name = request.POST['company_name']


    new_company = Company_model(company_name=company_name, members=founder_json)
    new_company.save()
    founder = User.objects.filter(pk=founder_id)[0]
    founder.company = new_company
    founder.save()

    return HttpResponse("创建新公司成功")

# @login_required
def join_company(request):
    """
    选择一个公司加入
    ./game/join_company POST
    company_name: 要加入的公司名
    user_id: 要加入的用户的id
    """
    company_name = request.POST['company_name']
    user_id = request.POST['user_id']
    company = Company_model.objects.get(company_name=company_name)
    user = User.objects.get(pk=user_id)
    user.company = company
    user.save()

    return HttpResponse("加入公司成功")

# TODO: 创建房间和加入房间
# def

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
                    time=datetime.now())
    record.save()
    record.players.add(user)

    profile.current_game = record
    profile.save()

    return HttpResponse('ok')

'''
游戏内的
'''
@login_required
def long_loan(request):
    """
    ./game/long_loan POST
    value: 贷款额
    year: 贷款年限
    """
    if request.method == 'POST':
        record, c = get_company(request)
        params = json.loads(request.body)
        c.long_loan(**params)

        record.status = jsonpickle.dumps(c)
        record.save()
        return HttpResponse('ok')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def short_loan(request):
    """
    ./game/short_loan POST
    user_id: 用户id
    value: 贷款额
    """
    company_id = get_company_id(request)
    # value = request.POST['value']
    game_obj[company_id].short_loan(**request.POST)

    return HttpResponse('ok')


@login_required
def order_raw_material(request):
    """
    ./game/order_raw_material POST
    user_id: 用户id
    order: 原材料订单，json格式，例如order = {'r1': 3, 'r2': 2, 'r3': 1, 'r4': 1}
    """
    company_id = get_company_id(request)
    json_order = request.POST['order']
    # 把json的字符串转成数字
    for key, value in json_order.items():
        json_order[key] = int(value)

    game_obj[company_id].order_raw_material(json_order)

    return HttpResponse('ok')


@login_required
def buy_workshop(request):
    """
    ./game/buy_workshop POST
    user_id: 用户id
    workshop_type: str, 'big','medium','small'
    slot_id: 用户点的那块地的id
    """
    company_id = get_company_id(request)
    workshop_type = request.POST['workshop_type']
    slot_id = request.POST['slot_id']

    game_obj[company_id].buy_workshop(workshop_type, slot_id)

    return HttpResponse('ok')


@login_required
def new_line(request):
    """
    ./game/neww_line POST
    user_id: 用户id
    line_type: 生产线类型，'Flex','Hand','Auto'
    product_type: 产品类型，'p1', 'p2', 'p3', 'p4'
    workshop_id: 在哪个厂房里面点的新建生产线
    slot_id: 生产线放在厂房的哪一格
    """
    company_id = get_company_id(request)
    line_type = request.POST['line_type']
    product_type = request.POST['product_type']
    workshop_id = request.POST['workshop_id']
    # slot_id =


def test_param(request, msg):
    return HttpResponse(msg)



'''
helper methods
'''
def get_company(request):
    """
    根据request的session，判断哪个用户点的
    返回相应的记录和游戏object
    """
    user = get_user(request)
    return user.Profile.current_game, jsonpickle.loads(user.Profile.current_game.status)
