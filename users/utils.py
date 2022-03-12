import json
from admins.models import *
import uuid


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}
    print('Cart : ', cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    for i in cart:
        product = Product.objects.get(id=i)
        total = (product.last_price * cart[i]["quantity"])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product' : product,
            'quantity':cart[i]['quantity'],
            'get_total':total
            }
        items.append(item)
    return {'order':order,'items':items}

def getRefcode(request):
    refCode = str(uuid.uuid4()).replace('_','')[:15]
    return refCode