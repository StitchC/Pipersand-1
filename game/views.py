from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from game.models import Company as Company_model
from game.models import MyUser as User
# Create your views here.

import sys
sys.path.append("C:/Users/67089/Documents/GitHub/Pipersand")
from Sandbox.core.Company import Company

import json

# 每次开始游戏，对会在字典里面创建一个key为company_id的Company object
game_obj = {}

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
    User.objects.create_user(username, email, password)
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
    if user:
        login(request, user)
        # Redirect to a success page.
    else:
        HttpResponse("fuk you")

def logout(request):
    logout(request)


def changing_password(request):
    """
    ./modify_password POST
    new_password: 新密码
    """
    new_password = request.POST['new_password']
    u =
    u.set_password(new_password)
    u.save()
    return HttpResponse('ok')


def create_company(request):
    """
    一个用户创建一个company，加入到company list里面
    ./game/create_company POST
    company_name: 公司名
    user_id: 创建者的id
    """
    company_name = request.POST['company_name']
    founder_id = request.POST['user_id']
    founder_json = json.dumps([founder_id])

    new_company = Company_model(company_name=company_name, members=founder_json)
    new_company.save()
    founder = User.objects.filter(pk=founder_id)[0]
    founder.company = new_company
    founder.save()

    return HttpResponse("创建新公司成功")

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

def start_game(request):
    """
    创建或者加入了公司的玩家可以选择一个房间点开始游戏
    ./game/start_game POST
    room_id: 房间号

    在字典里面创建一个object, key是user_id对应的company_id
    user_id: 点开始游戏那个用户的id
    """
    user_id = self.request.GET['user_id']
    company_id = User.objects.get(pk=user_id).company.id
    if company_id not in game_obj:
        game_obj[company_id] = Company()

    return HttpResponse('ok')





'''
helper methods
'''
def check_ready_to_start():
    """
    check是否可以开始
    """
    if len(game_obj) == 10:
        return True
    else:
        return False

def get_company_id(request):
    """
    用user_id来get company_id
    """
    user_id = request.POST.pop('user_id')
    company_id = User.objects.get(pk=user_id).company.id
    return company_id








'''
游戏内的
'''
@login_required
def long_loan(request):
    """
    ./game/long_loan POST
    user_id: 用户id
    value: 贷款额
    year: 贷款年限
    """
    company_id = get_company_id(request)
    # value = request.POST['value']
    # year = request.POST['year']
    game_obj[company_id].long_loan(**request.POST)

    return HttpResponse('ok')

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
