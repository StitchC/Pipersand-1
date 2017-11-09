from django.db import models
from django.db.models import SET_NULL
from django.contrib.auth.models import User

import json
from typing import List
# Create your models here.
# class pipersand(models.Model):
#     def __init__(self):
#
# class MyUser(User):
#     # username和password在父类里面有
#     company = models.ForeignKey('Company', on_delete=SET_NULL, null=True)
class Profile(models.Model):
    current_game = models.OneToOneField('Record', default=None, null=True, on_delete=SET_NULL)
    user = models.OneToOneField(User, default=None, related_name='Profile')


# class Company(models.Model):
#     company_name = models.CharField(max_length=20)
#     members = models.CharField(max_length=200)
#
#     def get_member(self):
#         return json.loads(self.members)


class Record(models.Model):
    time = models.DateTimeField()   # 存的是python里面的datetime.datetime instance
    status = models.TextField()
    player = models.ForeignKey(User, default=None, null=True)
    # players = models.CharField(max_length=100) # 一个公司最多5个人，每个人的id不超过20
    parent = models.OneToOneField('self', on_delete=models.CASCADE, related_name='child',
                                  default=None, null=True)
