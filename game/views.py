from django.shortcuts import render
from django.http import HttpResponse
from game.models import Company as Company_model
from game.models import User
# Create your views here.

import sys
sys.path.append("C:/Users/67089/Documents/GitHub/Pipersand")
from Sandbox.core.Company import Company

import json

companys = [None for _ in range(10)]

def home(request):
    return HttpResponse("welcome")

def create_user(request):
    """
    ./game/register POST
    name: 用户名
    password: 密码
    """
    name = request.POST['name']
    password = request.POST['password']
    User.objects.create(name=name, password=password)
    return HttpResponse("创建新用户成功")


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
    # User.objects.filter(pk=founder_id).update(company=new_company)

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


def long_loan(request):
    company_id = request.POST['company_id']
    value = request.POST['value']
    year = request.POST['year']
    game_obj[company_id].long_loan(value, year)


# class Game(object):
#     def __init__(self):
#         self.start = 0
#     def add(self):
#         self.start += 1
#
#
# game_obj = [None for _ in range(10)]
# def invoke(request):
#     game_obj[0] = Game()
#     return HttpResponse("started game!")
#
# def add(request):
#     game_obj[0].add()
#     return HttpResponse(game_obj[0].start)
