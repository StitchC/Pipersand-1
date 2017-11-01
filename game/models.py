from django.db import models
from django.db.models import SET_NULL
from django.contrib.auth.models import User

import json
from typing import List
# Create your models here.
# class pipersand(models.Model):
#     def __init__(self):
#
class MyUser(User):
    # name = models.CharField(max_length=20)
    # password = models.CharField(max_length=30)
    # username和password在父类里面有
    company = models.ForeignKey('Company', on_delete=SET_NULL, null=True)


class Company(models.Model):
    company_name = models.CharField(max_length=20)
    members = models.CharField(max_length=200)

    # password = model.CharField(max_length=30)

    def get_member(self):
        return json.loads(self.members)
