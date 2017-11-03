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


class Company(models.Model):
    company_name = models.CharField(max_length=20)
    members = models.CharField(max_length=200)

    # password = model.CharField(max_length=30)

    def get_member(self):
        return json.loads(self.members)


class Record(models.Model):
    time = models.DateTimeField()   # 存的是python里面的datetime.datetime instance
    status = models.TextField()
    players = models.ManyToManyField(User)
    # players = models.CharField(max_length=100) # 一个公司最多5个人，每个人的id不超过20
    parent = models.OneToOneField('self', on_delete=models.CASCADE, related_name='child',
                                  default=None, null=True)
    # child = models.OneToOneField('self', on_delete=models.CASCADE, related_name='parent',
    #                               default=None)
