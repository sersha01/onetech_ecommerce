from django.views.decorators.cache import never_cache
from decouple import config
from django.http import JsonResponse
from twilio.rest import Client
import random
from django.shortcuts import redirect, render
from admins.models import *
from django.contrib.auth import logout, login, authenticate
from .models import Address, User
from .forms import AddressForm, UserForm

# Create your views here.
@never_cache
def home(request):
    # if request.session.has_key('user'):
        products = Product.objects.all()
        return render(request, 'users/blog.html', {'products':products})
    # return redirect('email_login') 

@never_cache
def sign_up(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_login')
    return render(request, 'users/sign_up.html', {'form':form})

@never_cache
def email_login(request):
    if request.session.has_key('user'):
        return render(request, 'users/index.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, username = email,password = password)
        print(user)
        if user is not None:
            if user.status == True:
                login(request,user)
                return redirect('home')
            else:
                return redirect('block')
        else:
            return render(request, 'users/sign_in.html', {'message':'email or password is error'})
    return render(request, 'users/sign_in.html')

@never_cache
def otp_login(request):
    global num
    if request.method == 'POST':
        phone = request.POST.get('number')
        user = None
        try:
            user = User.objects.get(phone=phone)
        except:
            return render(request, 'users/phone.html', {'message':'This nomber is not exist'})
        if user is not None:
            num = random.randrange(123456,999999)
            print(num)
            account_sid = config('account_sid')
            auth_token  = config('auth_token')
            client = Client(account_sid, auth_token)
            message = client.messages.create(  
                              messaging_service_sid=config('messaging_service_sid'), 
                              body=str(num),      
                              to='+919061427297' 
                            ) 
            print(message.sid)
            return render(request, 'users/otp.html', {'number':phone})
    return render(request, 'users/phone.html')

@never_cache
def logoutView(request):
    logout(request)
    return redirect('email_login')

@never_cache
def otp_check(request,number = None):
    if request.method == 'POST' and number is not None:
        otp = request.POST.get('otp')
        user = User.objects.get(phone=number)
        if str(otp) == str(num):
            if user.status == True:
                login(request, user)
                return redirect('home')
            else:
                return redirect('block')
        else:
            return render(request, 'users/otp.html', {'message':'OTP is not matching'})
    return render(request, 'users/otp.html')

@never_cache
def single_product(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'users/h.html', {'product':product})

@never_cache
def block(request):
    return render(request, 'users/404.html')

@never_cache
def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:
                product_id = None
                product_id = request.GET.get('id')
                action = request.GET.get('action')
                user = request.user
                order = Order.objects.get(user=user,order_status=False)
                product = Product.objects.get(id=product_id)
                order_item = OrderItem.objects.get(product=product, order=order)
                if str(action) == 'incriment':
                    quantity = int(order_item.quantity) + 1
                    OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
                elif str(action) == 'dicriment' and order_item.quantity > 1:
                    quantity = int(order_item.quantity) - 1
                    OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
                items = order.orderitem_set.all()
                item = OrderItem.objects.get(product=product, order=order)
                response = {'quantity': quantity,'id':product_id, 'cart_total':order.get_cart_total, 'item_total': item.get_total, 'total_items':order.get_cart_items,'stock':'items.product.stock' }
                return JsonResponse(response)
            except:
                try:
                    user = request.user
                    order = Order.objects.get(user=user,order_status=False)
                    items = order.orderitem_set.all()
                except:
                    order = []
                    items = {}
        elif request.method == 'POST':
            product_id = request.POST.get('product_id')
            user = request.user
            order , created = Order.objects.get_or_create(user=user,order_status=False)
            product = Product.objects.get(id=product_id)
            try:
                item = None
                item = OrderItem.objects.get(product=product,order=order)
            except:
                pass
            if item is not None:
                quantity = int(item.quantity) + 1
                OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
            else:
                OrderItem.objects.create(product=product,order=order,quantity=1)
            items = order.orderitem_set.all()
        else:
            try:
                user = request.user
                order = Order.objects.get(user=user,order_status=False)
                items = order.orderitem_set.all()
            except:
                order = []
                items = {}
    else:
        order = []
        items = {}
    return render(request, 'users/cart.html',{'order':order,'items':items})

@never_cache
def remove(request,id):
    user = request.user
    order = Order.objects.get(user=user,order_status=False)
    product = Product.objects.get(id=id)
    order_item = OrderItem.objects.get(product=product, order=order)
    order_item.delete()
    return redirect('add_to_cart')

@never_cache
def checkout(request):
    user = request.user
    order = Order.objects.get(user=user,order_status=False)
    items = order.orderitem_set.all()
    address = Address.objects.filter(user=user)
    return render(request, 'users/checkout.html', {'order':order,'items':items,'address':address})

@never_cache
def proceed(request):
    print('yes')
    if request.method == 'POST':
        payment = request.POST.get('payment')
        status = True if str(payment) != 'COD' else False
        print(status)
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)
        user = request.user
        Order.objects.filter(user=user,order_status=False).update(order_status=True, address=address, payment=status)
        response = {'':''}
        return JsonResponse(response)
    return redirect('home')

@never_cache
def cancel(request,id):
    order = Order.objects.filter(id=id)
    order.update(status='UserCancelled')
    return redirect('user_orders')

# @never_cache
# def view_cart(request):
#     if request.user.is_authenticated:
#         user = request.user
#         order = Order.objects.get(user=user,order_status=False)
#         items = order.orderitem_set.all()
#     else:
#         order = []
#         items = {}
#     return render(request, 'users/checkout.html', {'order':order,'items':items})

@never_cache
def add_address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')
    return render(request, 'users/add_address.html', {'form':form})

# def user_orders(request):
#     user = request.user
#     orders = Order.objects.filter(user=user,order_status=True).order_by('-date_order')
#     items = []
#     for order in orders:
#         item = order.orderitem_set.all()
#         items.append(item)
#     return render(request, 'users/orders.html', {'orders':orders, 'items':items})

def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user,order_status=True).order_by('-date_order')
    address = Address.objects.filter(user=user)
    items = []
    for order in orders:
        item = order.orderitem_set.all()
        items.append(item)
    return render(request, 'users/profile.html', {'orders':orders, 'items':items,'address':address})


# def cart(request):
#     global valu
#     valu = 1
#     print('suc')
#     stock = 5
#     try:
#         val = int(request.POST.get('action'))
#         print(val)
#         if stock > val:
#             print('hello')
#             valu = val + 1
#             print(valu)
#         else:
#             print('hellooo') 
#             valu = stock
#     except:
#         pass
#     user = request.user
#     order = Order.objects.get(user=user,order_status=False)
#     items = order.orderitem_set.all()
#     return render(request, 'users/cart.html',{'order':order,'items':items})

# def view(request):
#     user = request.user
#     order , created = Order.objects.get_or_create(user=user,order_status=False)
#     items = order.orderitem_set.all()
#     return render(request, 'users/cart.html',{'order':order,'items':items})