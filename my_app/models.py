from __future__ import unicode_literals

from django.db import models

class Order(models.Model):
    time_order = models.TimeField(auto_now_add=True)
    buy_product = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    byn = models.FloatField(default=0)
    byr = models.IntegerField(default=0)
    comment = models.CharField(max_length=1000, null=True)
