#coding=utf-8
from django.shortcuts import render
from models import Order
from forms import OrderForm
from django.shortcuts import redirect
from utils import total_sum
import datetime


def order_form(request):
    time_order = datetime.datetime.now()
    cur_hour = time_order.hour
    cur_minute = time_order.minute
    if request.method == 'POST':
        if request.POST.get('changed_order_id') is not None:
            changed_order_id = request.POST.get('changed_order_id')
            new_buy_product = request.POST.get('new_buy_product')
            new_name = request.POST.get('new_name')
            new_email = request.POST.get('new_email')
            new_byn = request.POST.get('new_byn')
            new_byr = request.POST.get('new_byr')
            new_comment = request.POST.get('new_comment')
            if ',' in new_byn:
                new_byn = new_byn.replace(',', '.')
            if ',' in new_byr:
                new_byr_list = new_byr.split(',')
                new_byr = new_byr_list[0]
            elif '.' in new_byr:
                new_byr_list = new_byr.split('.')
                new_byr = new_byr_list[0]
            Order.objects.filter(id=changed_order_id).update(buy_product=new_buy_product, name=new_name,
                                                             email=new_email, byn=new_byn , byr=new_byr,
                                                             comment=new_comment)
            update_order = Order.objects.filter(id=changed_order_id).get()
            return redirect(order_table)
        else:
            form = OrderForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order = Order.objects.create(buy_product = data['buy_product'], name = data['name'], email = data['email'], byn = data['byn'], byr = data['byr'], comment = data['comment'])

                return redirect(thanks_for_order)
            context = {'order_form': form}
            return render(request, 'order_form.html', context)
    else:
        if cur_hour<=14 or cur_hour==15 and cur_minute==0:
            context = {'order_form': OrderForm()}
            return render(request, 'order_form.html', context)
        else:
            time_message = 'Заказы принимаются до 15.00'
            context = {'time_message': time_message}
            return render(request, 'order_form.html', context)

def order_table(request):

        list_orders = Order.objects.filter()
        if request.method == 'POST':
            update = request.POST.get('update')
            delete = request.POST.get('delete')
            checked_order = request.POST.get('checked')
            if checked_order is not None:
                if update is not None:
                    changed_order = Order.objects.filter(id = checked_order).get()
                    context = {'changed_order': changed_order}
                    return render(request, 'order_form.html', context)
                elif delete is not None:
                    delete_order = Order.objects.filter(id = checked_order).get()
                    delete_order.delete()
                    new_list_orders = Order.objects.filter()
                    context = {'orders': new_list_orders, 'totals': total_sum()}
                    return render(request, 'order_table.html', context)
            else:
                message = 'Вы не выбрали заказ!'
                context = {'orders': list_orders, 'totals': total_sum(), 'message': message}
                return render(request, 'order_table.html', context)

        else:
            context = {'orders': list_orders, 'totals': total_sum()}
            return render(request, 'order_table.html', context)



def thanks_for_order(request):
    if request.user.is_authenticated():
        return redirect(order_table)
    else:
        thanks = 'Ваш заказ принят. Спасибо, что выбрали нашу компанию!'
        context = {'thanks': thanks}
        return render(request, 'order_table.html', context)


