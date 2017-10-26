from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

'''
import 整个Sandbox2过来，invoke的时候创建一个game对象，
'''
class Game(object):
    def __init__(self):
        self.start = 0
    def add(self):
        self.start += 1

game_obj = None
def invoke(request):
    global game_obj
    game_obj = Game()
    return HttpResponse("started game!")

def add(request):
    global game_obj
    game_obj.add()
    return HttpResponse(game_obj.start)

def long_loan(request):
    global game_obj

    company_id = request.POST['company_id']
    value = request.POST['value']
    year = request.POST['year']
    game_obj[company_id].long_loan(value, year)
