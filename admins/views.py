from django.shortcuts import redirect, render
from users.models import User
from .models import *
from .forms import ProductForm

# Create your views here.
def sup_home(request):
    if request.session.has_key('admin'):
        return render(request, 'admins/index.html')
    return redirect('login')

def test(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    return render(request, 'users/test.html', {'form':form})

def products(request):
    if request.session.has_key('admin'):
        products = Product.objects.all().order_by('id')
        return render(request, 'admins/products-list.html',{'products':products})
    else:
        return redirect('login')
    return render(request, 'admins/products-list.html')


def orders(request):
    orders = Order.objects.filter(order_status=True)
    # items = []
    # array = []
    # for order in orders:
    #     item = order.orderitem_set.all()
    #     array.append(item)
    #     items.append(array)
    #     array = []
    # print(items)
    # for item in items:
    #     for i in item:
    #         print(i)
    return render(request, 'admins/orders_list.html',{'orders':orders})


def order(request,id):
    order = Order.objects.get(id=id)
    items = order.orderitem_set.all()
    return render(request, 'admins/order.html',{'items':items,'orders':order})


def product(request,id,edit=None):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        edit=None
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = ProductForm( instance=product)
    return render(request, 'admins/product.html', {'form':form, 'product':product, 'edit':edit})

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    return render(request, 'admins/add_product.html', {'form':form})

def customers(request):
    if request.session.has_key('admin'):
        users = User.objects.all().order_by('id')
        return render(request, 'admins/customers-list.html',{'users':users})
    else:
        return redirect('login')
    return render(request, 'admins/customers-list.html')

def customers_sts(request,id):
    if request.session.has_key('admin'):
        user = User.objects.get(id=id)
        if user.status == True:
            User.objects.filter(id=id).update(status=False)
            return redirect('customers')
        else:
            User.objects.filter(id=id).update(status=True)
            return redirect('customers')
    else:
        return redirect('login')
    return render(request, 'admins/customers-list.html')

def login(request):
    if request.session.has_key('admin'):
        return redirect('sup_home')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'sersha@gmail.com' and password == 'sersha':
            request.session['admin'] = email
            return redirect('sup_home')
    return render(request, 'admins/sign_in.html')

def sup_logout(request):
    try:
        del request.session['admin']
    except:
        pass
    return redirect('login')

def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')

def order_update(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        selected = request.POST.get('selected')
        order = Order.objects.filter(id=order_id)
        if selected == 'Pending':
            status = 'Pending'
        elif selected == 'Shipped':
            status = 'Shipped'
        elif selected == 'Delivered':
            status = 'Delivered'
        else:
            status = 'Cancelled'
        order.update(status=status)
        print(status)
    return redirect('orders')
