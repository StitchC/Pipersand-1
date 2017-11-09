from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed,
    HttpResponseBadRequest)

from game.models import Record, Profile
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

# import sys
# sys.path.append("C:/Users/67089/Documents/GitHub/Pipersand")
from Sandbox.core.Company import Company

import json
import jsonpickle
from datetime import datetime



'''
游戏内的
'''
@login_required
def roll_back(request):
    """
    ./game/util/roll_back POST
    """
    if request.method == 'POST':
        user = get_user(request)
        # 新记录的id
        new_id = user.Profile.current_game.id
        # 改current_game pointer到旧记录
        profile = user.Profile
        profile.current_game = profile.current_game.parent
        profile.save()
        # 删掉新记录
        Record.objects.get(pk=new_id).delete()
        return HttpResponse("ok")
    else:
        return HttpResponseNotAllowed(['POST'])



@login_required
def long_loan(request):
    """
    ./game/long_loan POST
    value: 贷款额
    year: 贷款年限
    """
    if request.method == 'POST':
        user, c = get_user_company(request)
        params = json.loads(request.body)

        c.long_loan(**params)
        forward_record(user, c)
        return HttpResponse('ok')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def cmd_proxy(request, cmd):
    """
    处理所有API文档里面的所有命令，参数看文档
    ./game/(\w+) POST json
    """
    if request.method == 'POST':
        user, c = get_user_company(request)
        params = json.loads(request.body)

        getattr(c, cmd)(**params)
        forward_record(user, c)
        return HttpResponse('ok')
    else:
        return HttpResponseNotAllowed(['POST'])



# @login_required
# def short_loan(request):
#     """
#     ./game/short_loan POST
#     value: 贷款额
#     """
#     if request.method == 'POST':
#         user, c = get_user_company(request)
#
#     return HttpResponse('ok')
#
#
# @login_required
# def order_raw_material(request):
#     """
#     ./game/order_raw_material POST
#     user_id: 用户id
#     order: 原材料订单，json格式，例如order = {'r1': 3, 'r2': 2, 'r3': 1, 'r4': 1}
#     """
#     company_id = get_company_id(request)
#     json_order = request.POST['order']
#     # 把json的字符串转成数字
#     for key, value in json_order.items():
#         json_order[key] = int(value)
#
#     game_obj[company_id].order_raw_material(json_order)
#
#     return HttpResponse('ok')
#
#
# @login_required
# def buy_workshop(request):
#     """
#     ./game/buy_workshop POST
#     user_id: 用户id
#     workshop_type: str, 'big','medium','small'
#     slot_id: 用户点的那块地的id
#     """
#     company_id = get_company_id(request)
#     workshop_type = request.POST['workshop_type']
#     slot_id = request.POST['slot_id']
#
#     game_obj[company_id].buy_workshop(workshop_type, slot_id)
#
#     return HttpResponse('ok')
#
#
# @login_required
# def new_line(request):
#     """
#     ./game/neww_line POST
#     user_id: 用户id
#     line_type: 生产线类型，'Flex','Hand','Auto'
#     product_type: 产品类型，'p1', 'p2', 'p3', 'p4'
#     workshop_id: 在哪个厂房里面点的新建生产线
#     slot_id: 生产线放在厂房的哪一格
#     """
#     company_id = get_company_id(request)
#     line_type = request.POST['line_type']
#     product_type = request.POST['product_type']
#     workshop_id = request.POST['workshop_id']
#     # slot_id =


def test_param(request, msg):
    return HttpResponse(msg)



'''
helper methods
'''
def get_user_company(request):
    """
    根据request的session，判断哪个用户点的
    返回相应的user, game_object
    """
    user = get_user(request)
    return user, jsonpickle.loads(user.Profile.current_game.status)


def forward_record(user, c):
    """
    根据c(current_game object)
    向前更新user的current_game Record
    """
    # 创建一个新记录
    record = Record(status=jsonpickle.dumps(c),
                    time=timezone.now(),
                    player=user,
                    parent=user.Profile.current_game)
    record.save()

    # 把user的current_game指向这个新记录
    profile = user.Profile
    profile.current_game = record
    profile.save()


# @login_required
# def create_company(request):
#     """
#     一个用户创建一个company，加入到company list里面
#     ./game/create_company POST
#     company_name: 公司名
#     """
#     company_name = request.POST['company_name']
#
#
#     new_company = Company_model(company_name=company_name, members=founder_json)
#     new_company.save()
#     founder = User.objects.filter(pk=founder_id)[0]
#     founder.company = new_company
#     founder.save()
#
#     return HttpResponse("创建新公司成功")
#
# # @login_required
# def join_company(request):
#     """
#     选择一个公司加入
#     ./game/join_company POST
#     company_name: 要加入的公司名
#     user_id: 要加入的用户的id
#     """
#     company_name = request.POST['company_name']
#     user_id = request.POST['user_id']
#     company = Company_model.objects.get(company_name=company_name)
#     user = User.objects.get(pk=user_id)
#     user.company = company
#     user.save()
#
#     return HttpResponse("加入公司成功")
#
# # TODO: 创建房间和加入房间
# # def
