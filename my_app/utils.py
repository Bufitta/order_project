from models import Order

def total_sum():
    orders = Order.objects.filter()
    total = 0
    total_byn = 0
    total_byr = 0
    for order in orders:
        byn = order.byn
        byr = order.byr
        new_byr = float(byr)/10000
        total_byn += byn
        total_byr += byr
        total += (byn+new_byr)
    total = round(total,2)
    return {'total': total, 'total_byr': total_byr, 'total_byn': total_byn}




