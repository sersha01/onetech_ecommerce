from http.client import responses
from django.db.models import Q,Min,Max
from tkinter import S
from pconst import const
import json
from re import T
from django.views.decorators.cache import never_cache
from decouple import config
from django.http import JsonResponse
from twilio.rest import Client
from django.shortcuts import redirect, render
from admins.models import *
from django.contrib.auth import logout, login, authenticate
from admins.views import offers, product
from .models import Address, User
from .forms import AddressForm, UserForm
from .utils import *
from django.template.loader import render_to_string


@never_cache
def home(request):
    check = False
    products = Product.objects.all().order_by('?')
    brands = Brand.objects.all()
    wishList = []
    if request.user.is_authenticated:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart ={}
        user = request.user
        if bool(cart):
            order , created = Order.objects.get_or_create(user=user,order_status=False,buy_now=False)
            for i in cart:
                product = Product.objects.get(id=i)
                try:
                    item = OrderItem.objects.get(product=product, order=order)
                except:
                    item = OrderItem.objects.create(product=product,order=order,quantity=0)
                quantity = int(item.quantity) + cart[i]['quantity']
                OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
            check = True
        wishList = [item.product.id for item in WishList.objects.filter(user=user)]
    minPrice = Product.objects.aggregate(Min('price'))
    maxPrice = Product.objects.aggregate(Max('price'))
    return render(request, 'users/blog.html', {'products':products,'check':check,'brands':brands,'minPrice':minPrice['price__min'],
    'maxPrice':maxPrice['price__max'], 'wishList':wishList})

@never_cache
def sign_up(request, **kwargs):
    ref_code = kwargs.get('ref_code')
    form = UserForm()
    if request.method == 'POST':
        number = request.POST.get('phone')
        otp = request.POST.get('otp')
        check = otpCheck(request, number, otp)
        if check == False:
            try:
                const.stored = UserForm(request.POST)
            except:
                pass
            return render(request, 'users/sign_up.html',{'otp':True,'number':number,'message':'invalid OTP'})
        else:
            try:
                if const.stored != None:
                    form = const.stored
            except:
                form = UserForm(request.POST)
            if ref_code == None:
                    if form.is_valid():
                        form.save()
                        username = form['username'].value()
                        User.objects.filter(username=username).update(ref_id = getRefcode(request))
                        user = User.objects.get(username=username)
                        SignupCoupon.objects.create(name='Normal', user=user, price='10%')
                        login(request,user)
                        return redirect('home')
            else:
                try:
                    user = None
                    user = User.objects.get(ref_id=ref_code)
                except:
                    pass
                if user is not None:
                    if form.is_valid():
                        form.save()
                        SignupCoupon.objects.create(name='ReferredBy', user=user, price='8%')
                        username = form['username'].value()
                        User.objects.filter(username=username).update(ref_id = getRefcode(request))
                        user = User.objects.get(username=username)
                        SignupCoupon.objects.create(name='ReferredTo', user=user, price='18%')
                        login(request,user)
                        return redirect('home')
    return render(request, 'users/sign_up.html', {'form':form})

@never_cache
def email_login(request):
    if request.session.has_key('user'):
        return render(request, 'users/index.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email,password = password)
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
    if request.method == 'POST':
        phone = request.POST.get('number')
        number = '+91' + str(phone)
        user = None
        try:
            user = User.objects.get(phone=phone)
        except:
            return render(request, 'users/phone.html', {'message':'This nomber is not exist'})
        if user is not None:
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)
            verification = client.verify \
                                .services(config('messaging_service_sid')) \
                                .verifications \
                                .create(to=number, channel='sms')
            return render(request, 'users/otp.html', {'number':phone})
    return render(request, 'users/phone.html')

def otp_l(request):
    phone = request.POST.get('number')
    number = '+91' + str(phone)
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    verification = client.verify \
                        .services(config('messaging_service_sid')) \
                        .verifications \
                        .create(to=number, channel='sms')
    return render(request, 'users/phone.html')


@never_cache
def logoutView(request):
    logout(request)
    return redirect('home')

@never_cache
def otp_check(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        number = request.POST.get('number')
        phone = '+91' + str(number)
        account_sid = config('account_sid')
        auth_token = config('auth_token')
        if len(otp) < 6:
            return render(request, 'users/otp.html', {'number':number,'message':'OTP must be 6 digit'})
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                            .services(config('messaging_service_sid')) \
                            .verification_checks \
                            .create(to= phone, code= str(otp))
        if verification_check.status == 'approved':
            return redirect('email_login')
        else:
            return render(request, 'users/otp.html', {'number':number,'message':'invalid OTP'})
    return render(request, 'users/otp.html')


def otpCheck(request, number, otp):
    phone = '+91' + str(number)
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    if len(str(otp)) < 6:
        return render(request, 'users/otp.html', {'number':number,'message':'OTP must be 6 digit'})
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
                        .services(config('messaging_service_sid')) \
                        .verification_checks \
                        .create(to= phone, code= str(otp))
    if verification_check.status == 'approved':
        return True
    else:
        return False


def otp_check(request, number, otp):
    if request.method == 'POST':
        phone = '+91' + str(number)
        account_sid = config('account_sid')
        auth_token = config('auth_token')
        if len(otp) < 6:
            return render(request, 'users/otp.html', {'number':number,'message':'OTP must be 6 digit'})
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                            .services(config('messaging_service_sid')) \
                            .verification_checks \
                            .create(to= phone, code= str(otp))
        if verification_check.status == 'approved':
            return True
        else:
            return render(request, 'users/otp.html', {'number':number,'message':'invalid OTP'})


@never_cache
def single_product(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'users/product.html', {'product':product})

@never_cache
def block(request):
    return render(request, 'users/404.html')

@never_cache
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        Order.objects.filter(user=user,order_status=False,buy_now=True).delete()
        if request.method == 'GET':
            try:
                product_id = None
                product_id = request.GET.get('id')
                action = request.GET.get('action')
                order = Order.objects.get(user=user,order_status=False,buy_now=False)
                product = Product.objects.get(id=product_id)
                order_item = OrderItem.objects.get(product=product, order=order)
                if str(action) == 'increment':
                    if product.stock > order_item.quantity:
                        quantity = int(order_item.quantity) + 1
                        OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
                    else:
                        response = {'status':'error','id':product_id,'message':'Out of stock','available':product.stock}
                        return JsonResponse(response)
                elif str(action) == 'decrement' and order_item.quantity > 1:
                    quantity = int(order_item.quantity) - 1
                    OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
                items = order.orderitem_set.all()
                item = OrderItem.objects.get(product=product, order=order)
                response = {'status':'success','quantity': quantity,'id':product_id, 'cart_total':order.get_cart_total, 'item_total': item.get_total,
                 'total_items':order.get_cart_items,'stock':'items.product.stock' }
                return JsonResponse(response)
            except:
                try:
                    user = request.user
                    order = Order.objects.get(user=user,order_status=False,buy_now=False)
                    items = order.orderitem_set.all()
                except:
                    order = []
                    items = {}
        elif request.method == 'POST':
            product_id = request.POST.get('product_id')
            user = request.user
            order , created = Order.objects.get_or_create(user=user,order_status=False,buy_now=False)
            product = Product.objects.get(id=product_id)
            try:
                item = None
                item = OrderItem.objects.get(product=product,order=order)
            except:
                pass
            if item is not None:
                if product.stock > item.quantity:
                    quantity = int(item.quantity) + 1
                    OrderItem.objects.filter(product=product, order=order).update(quantity=quantity)
                else:
                    response = {'message':''}
                    return JsonResponse(response)
            elif product.stock > 0:
                OrderItem.objects.create(product=product,order=order,quantity=1)
            items = order.orderitem_set.all()
        else:
            try:
                user = request.user
                order = Order.objects.get(user=user,order_status=False,buy_now=False)
                items = order.orderitem_set.all()
            except:
                order = []
                items = {}
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
    return render(request, 'users/cart.html',{'order':order,'items':items})

@never_cache
def remove(request):
    user = request.user
    id = request.GET.get('id')
    order = Order.objects.get(user=user,order_status=False,buy_now=False)
    product = Product.objects.get(id=id)
    order_item = OrderItem.objects.get(product=product, order=order)
    order_item.delete()
    response = {'id':id}
    return JsonResponse(response)

@never_cache
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        signupCoupens = user.signupcoupon_set.filter(available = False, proceed=False)
        for coupen in signupCoupens:
            SignupCoupon.objects.filter(id=coupen.id).update(available = True)
        order = Order.objects.get(user=user,order_status=False,buy_now=False)
        items = order.orderitem_set.all()
        address = Address.objects.filter(user=user)
        signupCoupens = user.signupcoupon_set.filter(available = True)
        coupens = Coupen.objects.filter(remaining__gt=0)
        return render(request, 'users/checkout.html', {'order':order,'items':items,'address':address,'coupens':coupens, 'signupCoupens':signupCoupens})
    else:
        return redirect('email_login')

def wishItems(request):
    wishList = []
    order = {}
    if request.user.is_authenticated:
        user = request.user
        wishList = [item.product for item in WishList.objects.filter(user=user)]
        order = Order.objects.get(user=user,order_status=False,buy_now=False)
    count = len(wishList)
    return render(request, 'users/wish-list.html', {'products':wishList,'order':order,'count':count})


@never_cache
def proceed(request):
    if request.method == 'POST':
        payment = request.POST.get('payment')
        address_id = request.POST.get('address')
        coupen_type = request.POST.get('coupen')[:4]
        coupen_id = request.POST.get('coupen')[4:]
        status = True if str(payment) != 'COD' else False
        address = Address.objects.get(id=address_id)
        user = request.user
        try:
            order = Order.objects.get(user=user,order_status=False,buy_now=True)
        except:
            order = Order.objects.get(user=user,order_status=False,buy_now=False)
        items = order.orderitem_set.all()
        quantity_status = True
        outOfStock = []
        available = []
        for item in items:
            if item.quantity > item.product.stock:
                quantity_status = False
                outOfStock.append(str(item.product.id))
                available.append(str(item.product.stock))
        if quantity_status is True:
            if order.buy_now == True:
                Order.objects.filter(user=user,order_status=False,buy_now=True).update(order_status=True, address=address, payment=status, payment_method=payment, total=order.get_cart_total)
                if coupen_type == 'scpn':
                    SignupCoupon.objects.filter(id=coupen_id).update(proceed=True) #
                elif coupen_type == 'cupn':
                    coupen = Coupen.objects.filter(id=coupen_id)
                    print(coupen)
                    getCoupen = coupen.get(id=coupen_id)
                    coupen.update(remaining=int(getCoupen.remaining)-1) #
            else:
                Order.objects.filter(user=user,order_status=False,buy_now=False).update(order_status=True, address=address, payment=status, payment_method=payment, total=order.get_cart_total)
                if coupen_type == 'scpn':
                    SignupCoupon.objects.filter(id=coupen_id).update(proceed=True) #
                elif coupen_type == 'cupn':
                    coupen = Coupen.objects.filter(id=coupen_id)
                    print(coupen)
                    getCoupen = coupen.get(id=coupen_id)
                    coupen.update(remaining=int(getCoupen.remaining)-1) #
            for item in items :
                ordered = item.quantity
                prestocks = item.product.stock
                poststocks = prestocks - ordered
                productid = item.product.id
                Product.objects.filter(id = productid).update(stock = poststocks)
            response = {'status':'success','orderId':order.id}
        else:
            response = {'status':'error','outOfStock':outOfStock,'available':available}
        return JsonResponse(response)
    return redirect('home')

@never_cache
def cancel(request,id):
    order = Order.objects.filter(id=id)
    order.update(status='UserCancelled')
    return redirect('profile')


def coupen(request):
    if request.method == "POST":
        coupenId = request.POST.get('coupenId')[4:]
        coupenType = request.POST.get('coupenId')[:4]
        orderId = request.POST.get('orderId')
        action = request.POST.get('action')
        if coupenType == 'scpn':
            coupen = SignupCoupon.objects.get(id=coupenId)
        elif coupenType == 'cupn':
            coupen = Coupen.objects.get(id=coupenId)
        if action == 'apply':
            Order.objects.filter(id=orderId).update(coupen=int(coupen.price[:-1]))
            if coupenType == 'scpn':
                coupen = SignupCoupon.objects.filter(id=coupenId)
                coupen.update(available = False)
        else:
            Order.objects.filter(id=orderId).update(coupen=None)
            if coupenType == 'scpn':
                coupen = SignupCoupon.objects.filter(id=coupenId)
                coupen.update(available = True)
        order = Order.objects.get(id=orderId)
        return JsonResponse({'total':order.get_cart_total})


def filter_shop_products(request):
    minPrice = request.GET.get('range[minVal]')
    maxPrice = request.GET.get('range[maxVal]')
    brands=request.GET.getlist('brand[]')
    rams = request.GET.getlist('ram[]')
    roms = request.GET.getlist('rom[]')
    allProducts=Product.objects.all()
    if len(brands)>0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(rams)>0:
        allProducts = allProducts.filter(ram__in=rams).distinct()
    if len(roms)>0:
        allProducts = allProducts.filter(storage__in=roms).distinct()
    allProducts = allProducts.filter(Q(price__gt=minPrice, price__lt=maxPrice)).distinct()
    wishList = []
    if request.user.is_authenticated:
        user = request.user
        wishList = [item.product.id for item in WishList.objects.filter(user=user)]

    t = render_to_string('users/filtered_product.html',{'products':allProducts,'wishList':wishList})
    
    return JsonResponse({'data': t})

def dlt_address(request):
    add_id = request.GET.get('add_id')
    Address.objects.filter(id=add_id).delete()
    return JsonResponse({'id':add_id})

def edit_address(request,add_id):
    address = Address.objects.get(id=add_id)
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("profile")
    return render(request, 'users/edit_address.html', {'form':form,'id':add_id})

def homeBanner(request):
    banner = Banner.objects.all()
    products = Product.objects.all()
    orders = Order.objects.filter(order_status=True)
    arrivals = products.order_by('-date')[:4]
    sellingCound = OrderItem.objects.values('product').annotate(
        products_count=models.Count("product")
        ).filter(product__id__in=products, order__id__in=orders).order_by('-products_count')[:4]
    sellinglist = []
    for item in sellingCound:
        sellinglist.append(item['product'])
    selling = products.filter(id__in=sellinglist)
    return render(request, 'users/home.html', {'banners':banner, 'arrivals':arrivals, 'selling':selling})

# def removeCoupen(request):
#     if request.method == "POST":
#         coupenId = request.POST.get('coupenId')
#         orderId = request.POST.get('orderId')
#         coupen = SignupCoupon.objects.get(id=coupenId)
#         Order.objects.filter(id=orderId).update(coupen=NULL)
#         order = Order.objects.get(id=orderId)
#         return JsonResponse({'total':order.get_cart_total})


def buyNow(request,id):
    if request.user.is_authenticated:
        user = request.user
        signupCoupens = user.signupcoupon_set.filter(available = False, proceed=False)
        for coupen in signupCoupens:
            SignupCoupon.objects.filter(id=coupen.id).update(available = True)
        Order.objects.filter(user=user,order_status=False,buy_now=True).delete()
        order  = Order.objects.create(user=user,order_status=False,buy_now=True)
        product = Product.objects.get(id=id)
        OrderItem.objects.create(order=order,product=product)
        address = Address.objects.filter(user=user)
        signupCoupens = user.signupcoupon_set.filter(available = True)
        coupens = Coupen.objects.filter(remaining__gt=0)
        return render(request, 'users/checkout.html', {'order':order,'product':product,'address':address,
        'coupens':coupens, 'signupCoupens':signupCoupens})
    else:
        return redirect('email_login') 
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

def rpay(request):
    user = request.user
    address_id = request.GET.get('address')
    address = Address.objects.get(id=address_id)
    order = Order.objects.get(user=user,order_status=False,buy_now=False)
    response={'total':order.get_cart_total,'name':address.name,'email':address.user.username,'phone':address.number}
    return JsonResponse(response)

def order_return(request,id):
    order = Order.objects.filter(id=id)
    order.update(status='Return')
    return redirect('profile')

def texting(request):
    if request.method == 'POST':
        print('hy')
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
    return render(request, 'users/sign_up.html')

def wishList(request):
    productId = request.GET.get('product_id')
    product = Product.objects.get(id=productId)
    user = request.user
    products = WishList.objects.filter(user=user,product=product)
    wishList = [item.product for item in WishList.objects.filter(user=user)]
    print(len(wishList))
    if len(products) == 0 :
        WishList.objects.create(user=user,product=product)
        action = 'add'
        count = int(len(wishList)) + 1
    else:
        products.delete()
        action = 'remove'
        count = int(len(wishList)) - 1
    return JsonResponse({'id':productId,'action':action,'count':count})