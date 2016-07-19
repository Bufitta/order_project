#coding=utf-8
from django import forms

class OrderForm(forms.Form):
    buy_product = forms.CharField(label='Что купить',max_length=100)
    name = forms.CharField(label='Кому',max_length=100)
    email = forms.EmailField(label='Email', required=False)
    byn = forms.FloatField(label='Оплачено BYN', required=False, initial=0)
    byr = forms.IntegerField(label='Оплачено BYR', required=False, initial=0)
    comment = forms.CharField(label='Комментарий', max_length=1000, required=False)