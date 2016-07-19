#coding=utf-8
from django.shortcuts import render
from models import Order
from forms import OrderForm
from django.shortcuts import redirect
from utils import total_sum



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

def order_table(request):
        list_orders = Order.objects.filter()
        context = {'orders': list_orders, 'totals': total_sum()}
        return render(request, 'order_table.html', context)


def thanks_for_order(request):
    if request.user.is_authenticated():
        return redirect(order_table)
    else:
        thanks = 'Ваш заказ принят. Спасибо, что выбрали нашу компанию!'
        context = {'thanks': thanks}
        return render(request, 'order_table.html', context)


