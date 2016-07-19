#coding=utf-8
from django.shortcuts import render
from models import Order
from forms import OrderForm
from django.shortcuts import redirect
from utils import total_sum
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

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
            order = Order.objects.filter(id=changed_order_id).get()
            if new_byn!='':
                if ',' in new_byn:
                    new_byn = new_byn.replace(',', '.')
            else:
                new_byn=order.byn
            if new_byr!='':
                if ',' in new_byr:
                    new_byr_list = new_byr.split(',')
                    new_byr = new_byr_list[0]
                elif '.' in new_byr:
                    new_byr_list = new_byr.split('.')
                    new_byr = new_byr_list[0]
            else:
                new_byr=order.byr

            Order.objects.filter(id=changed_order_id).update(buy_product=new_buy_product, name=new_name,
                                                             email=new_email, byn=new_byn , byr=new_byr,
                                                             comment=new_comment)
            update_order = Order.objects.filter(id=changed_order_id).get()
            if update_order.email:
                my_order = u'Ваш заказ изменен!\nЧто вы собираетесь купить: {0:s}\nКомментарий по заказу: {1:s}'.format(update_order.buy_product, update_order.comment)
                send_mail(u'Изменение заказа', my_order, 'djangomailfororder@mail.ru',
                          [update_order.email])
            return redirect(order_table)
        else:
            form = OrderForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order = Order.objects.create(buy_product = data['buy_product'], name = data['name'], email = data['email'], byn = data['byn'], byr = data['byr'], comment = data['comment'])
                if cur_hour == 13 or cur_hour == 15 or (cur_hour == 15 and cur_minute == 0):
                    if User.objects.filter(is_superuser=True).count()>0:
                        user = User.objects.filter(is_superuser=True).get()
                        my_order = u'Заказ {0:s} для {1:s}\nПодробности на сайте http://127.0.0.1:8000/admin_page/'.format(order.buy_product, order.name)
                        send_mail(u'Поступил новый заказ', my_order, 'djangomailfororder@mail.ru', [user.email])
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

@login_required(login_url='/accounts/login/')
def order_table(request):
    if request.user.is_superuser:
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
                    if delete_order.email:
                        my_order = u'Ваш заказ {0:s} для {1:s} удален!'.format(delete_order.buy_product, delete_order.name)
                        send_mail(u'Удаление заказа', my_order, 'djangomailfororder@mail.ru',
                                  [delete_order.email])
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
    else:
        error_user = 'У вас недостаточно прав для просмотра и редактирования заказов'
        context = {'error': error_user}
        return render(request, 'order_table.html', context)

def thanks_for_order(request):
    if request.user.is_authenticated():
        return redirect(order_table)
    else:
        thanks = 'Ваш заказ принят. Спасибо, что выбрали нашу компанию!'
        context = {'thanks': thanks}
        return render(request, 'order_table.html', context)
