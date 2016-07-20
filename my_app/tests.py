from django.test import TestCase
from my_app.models import Order
from django.contrib.auth.models import User
from utils import total_sum

class MyTest(TestCase):
    def test_ok_create_order(self):
        data = {'buy_product': 'test', 'name': 'Alex', 'email': '1@mail.ru', 'byr': 10000, 'byn': 0, 'comment': 'test comment'}
        self.client.post('/form/', data)
        q_order = Order.objects.filter()
        self.assertEquals(q_order.count(), 1)
        order = q_order.get()
        self.assertEquals(order.buy_product, data['buy_product'])
        self.assertEquals(order.name, data['name'])
        self.assertEquals(order.email, data['email'])
        self.assertEquals(order.byr, data['byr'])
        self.assertEquals(order.comment, data['comment'])

    def test_ok_delete_order(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.is_superuser = True
        user.save()
        order = Order.objects.create(buy_product='test', name='Alex', email='1@mail.ru', byr=10000, byn=0,
                                     comment='test comment')
        checked_order = order.id
        delete = 'delete'
        data = {'checked': checked_order,'order': order, 'delete': delete}
        login = self.client.login(username='john', password='johnpassword')
        self.client.post('/admin_page/', data,)
        q_order = Order.objects.filter(id=order.id).count()
        self.assertEquals(q_order, 0)

    def test_ok_update_order(self):
        order = Order.objects.create(buy_product='test', name='Alex', email='1@mail.ru', byr=10000, byn=0,
                                     comment='test comment')
        changed_order_id = order.id
        data = {'changed_order_id': changed_order_id, 'new_buy_product': 'new product',
                'new_comment': 'new test comment', 'new_name': order.name, 'new_byn': order.byn, 'new_byr': order.byr}
        self.client.post('/form/', data)
        q_order = Order.objects.filter(id=changed_order_id)
        order = q_order.get()
        self.assertEquals(order.buy_product, data['new_buy_product'])
        self.assertEquals(order.comment, data['new_comment'])

    def test_ok_total_sum(self):
        Order.objects.create(buy_product='test1', name='Alex', email='1@mail.ru', byr=10000, byn=0,
                             comment='test1 comment')
        Order.objects.create(buy_product='test2', name='Nina', email='2@mail.ru', byr=0, byn=15.0,
                             comment='test2 comment')
        Order.objects.create(buy_product='test3', name='Vasya', email='3@mail.ru', byr=5000, byn=8.60,
                             comment='test3 comment')
        result = total_sum()
        self.assertEquals(result['total'], 25.1)
        self.assertEquals(result['total_byr'], 15000)
        self.assertEquals(result['total_byn'], 23.6)

