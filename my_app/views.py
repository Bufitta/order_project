#coding=utf-8
from django.shortcuts import render
from models import Order
from forms import OrderForm
from django.shortcuts import redirect



def order_form(request):
    if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order = Order.objects.create(buy_product = data['buy_product'], name = data['name'], email = data['email'], byn = data['byn'], byr = data['byr'], comment = data['comment'])
                return redirect(thanks_for_order)
            context = {'order_form': form}
            return render(request, 'order_form.html', context)
    else:
            context = {'order_form': OrderForm()}
            return render(request, 'order_form.html', context)


