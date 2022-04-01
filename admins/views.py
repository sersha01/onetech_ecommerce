
from bdb import Breakpoint
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from users.models import User
from .models import *
from .forms import BannerForm, ProductForm
import xlwt
import csv
from django.template.loader import render_to_string
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
        # breakpoint()
        products = Product.objects.all().order_by('id')
        for p in products:
        #     print(p.brand.category_off,'bbb')
        #     print(p.product_off.price,'lll')
            p.last_price
        #     print(p.last_price)
        return render(request, 'admins/products-list.html',{'products':products})
    else:
        return redirect('login')
    return render(request, 'admins/products-list.html')


def orders(request):
    orders = Order.objects.filter(order_status=True)
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
    return render(request, 'admins/dd.html', {'form':form, 'product':product, 'edit':edit})

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        rams = ['','1GB','2GB','4GB','6GB','8GB']
        roms = ['16GB','32GB','64GB','128GB','256GB']
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    return render(request, 'admins/add_product.html', {'form':form})

def copy(request,id):
    product = Product.objects.get(id=id)
    rams = ['','1GB','2GB','4GB','6GB','8GB']
    roms = ['16GB','32GB','64GB','128GB','256GB']
    last_price = product.last_price
    for ram in rams:
        for rom in roms:
            if ram == '':
                last_price += 1000
            elif ram == '1GB':
                last_price += 2000
            elif ram == '2GB':
                last_price += 3000
            elif ram == '4GB':
                last_price += 4000
            elif ram == '6GB':
                last_price += 5000
            elif ram == '8GB':
                last_price += 7000
            if rom == '16GB':
                last_price += 1000
            elif rom == '32GB':
                last_price += 2000
            elif rom == '64GB':
                last_price += 3000
            elif rom == '128GB':
                last_price += 4000
            elif rom == '256GB':
                last_price += 6000
            Product.objects.create(
                name = product.name,
                price = last_price,
                images1 = product.images1,
                images2 = product.images2,
                images3 = product.images3,
                ram = ram,
                storage = rom,
                camara = product.camara,
                battery = product.battery,
                processor = product.processor,
                display = product.display,
                stock = product.stock,
                brand = product.brand,
                date = product.date,
            )
    return redirect('products')

def customers(request):
    if request.session.has_key('admin'):
        users = User.objects.all().order_by('id')
        return render(request, 'admins/customers-list.html',{'users':users})
    else:
        return redirect('login')
    return render(request, 'admins/customers-list.html')

def customers_sts(request):
    id = request.GET.get('id')
    print(id)
    if request.session.has_key('admin'):
        print('hy')
        user = User.objects.get(id=id)
        print(user)
        if user.status == True:
            User.objects.filter(id=id).update(status=False)
        else:
            User.objects.filter(id=id).update(status=True)
        return JsonResponse({'id':id})
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

def delete(request):
    id = request.GET.get('id')
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')

def order_update(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        selected = request.POST.get('selected')
        order = Order.objects.filter(id=order_id)
        if selected == 'Pending' or selected == 'New':
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

def get_data(request, *args, **kwargs):
    # pending and not pending orders
    orders = Order.objects.filter(order_status=True)
    status = ["New","Pending","Shipped","Delivered","Cancelled","Return","UserCancelled"]
    pending = []
    pending_label = ["New","Pending","Shipped"]
    notPending = []
    notPending_label = ["Delivered","Cancelled","Return","UserCancelled"]
    for status in status:
        count = orders.filter(status=status).count()
        if status == "New" or status == "Pending" or status == "Shipped":
            pending.append(count)
        else:
            notPending.append(count)

    # soled items by brand
    brands = Brand.objects.all()
    sold = []
    product_arr =[]
    for brand in brands:
        products = brand.product_set.all()
        oders = Order.objects.filter(order_status=True)
        count = OrderItem.objects.filter(product__id__in=products, order__id__in=oders).count()
        print(count)
        sold.append(count)
        product_arr.append(str(brand))

    # whole solde by day
    counts = []
    days = []
    day = datetime.now() - timedelta(weeks=2)
    for i in range(14):
        start = day
        end = day + timedelta(days=1)
        count = Order.objects.filter(order_status=True,date_order__range=(start, end)).order_by('-date_order').count()
        days.append((day + timedelta(days=1)).strftime("%A"))
        counts.append(count)
        day += timedelta(days=1)

    count = User.objects.filter(last_login__startswith=datetime.now().date()).count()
    # passing whole data
    data = {
        'pending':{
            'data':pending,
            'labels':pending_label
        },
        'notPending':{
            'data':notPending,
            'labels':notPending_label
        },
        'brand':{
            'data':sold,
            'labels':product_arr
        },
        'by_day':{
            'data':counts,
            'labels':days
        }
    }
    return JsonResponse(data)

def coupens(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    off_products = Product.objects.exclude(product_off=None )
    off_brands = Brand.objects.exclude(category_off=None )
    for brand in off_brands:
        brand.items = products.filter(brand=brand).count()
    return render(request, 'admins/offers.html',{'off_products':off_products,'off_brands':off_brands,'products':products,'brands':brands})

def test1(request, *args, **kwargs):
    return render(request, 'admins/test1.html')

def br_delete(request,id):
    Brand.objects.filter(id=id).delete()
    return redirect('brands')

def br_add(request):
    name = request.POST.get('name')
    Brand.objects.create(name=name)
    return redirect('brands')

def brands(request):
    products = Product.objects.all()
    brands = Brand.objects.all().order_by('id')
    for brand in brands:
        brand.items = products.filter(brand=brand).count()
    return render(request, 'admins/brand.html',{'brands':brands})

def addOffer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        product_id = request.POST.get('product')
        offer = request.POST.get('offer')
        if name == 'Category':
            offerId = Offer.objects.create(name='Category',price=offer)
            Brand.objects.filter(id=brand_id).update(category_off=offerId)
        elif name == 'Product':
            offerId = Offer.objects.create(name='Product',price=offer)
            Product.objects.filter(id=product_id).update(product_off=offerId)
    return redirect('coupens')

def dltOffer(request,id):
    Offer.objects.filter(id=id).delete()
    return redirect('coupens')

def offers(request):
    if request.method == "POST":
        id = request.POST.get('typeId')
        val = request.POST.get('val')
        Offer.objects.filter(id=id).update(price=val)
    return redirect('coupens')


def sales(request):
    orders = Order.objects.all()
    years = []
    for i in range(15):
        val = 2010 + i
        years.append(val)
    if request.method == "POST":
        start = request.POST.get('from1')
        end = request.POST.get('from2')
        month = request.POST.get('from3')[-2:]
        year = request.POST.get('from4')
        if start != '':
            orders = Order.objects.filter(date_order__range=[start,end] ,order_status=True)
        elif month != '':
            orders = Order.objects.filter(date_order__month=month ,order_status=True)
        elif year != '':
            orders = Order.objects.filter(date_order__year=year ,order_status=True)
    return render(request, 'admins/sales.html', {'orders':orders,'years':years})


def exel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=SalesReport' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Order Id','Date Order','Payment Method','Total Amount']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    rows =  Order.objects.filter(order_status=True).values_list('id','date_order','payment_method','total')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

def exportCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SalesReport'+str(datetime.now())+'.csv'
    order = Order.objects.filter(date_order__month= 3 ,order_status=True)
    writer = csv.writer(response)
    writer.writerow(['Order Id','Date','Payment Method','Items','Total Amount'])
    try:
        report_total = 0
        for order in order:
            writer.writerow([order.id,order.date_order,order.payment_method,order.get_cart_items,order.get_cart_total])
            report_total = report_total + order.get_cart_total
        writer.writerow(['Total:-',report_total])
    except:
        # messages.error(request,'Empty Order')
        pass
    return response

def banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
    form = BannerForm()
    banner = Banner.objects.all()
    return render(request, 'admins/banner.html',{'form':form, 'banners':banner})

def searchCoustumor(request):
    value = request.GET.get('value')
    users = User.objects.filter(Q(name__icontains = value))
    t = render_to_string('admins/search-coustumor.html',{'users': users})
    return JsonResponse({'data':t})

def coupenManage(request):
    coupens = Coupen.objects.all()
    return render(request, 'admins/coupons.html',{'coupons':coupens})

def cpn_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        offer = request.POST.get('offer')
        stock = request.POST.get('stock')
        Coupen.objects.create(name = name, price = offer, remaining = stock)
    return redirect('coupen-manage')

def cpn_edit(request):
    if request.method == "POST":
        id = request.POST.get('typeId')
        val = request.POST.get('val')
        bal = request.POST.get('bal')
        name = request.POST.get('name')
        print(id,val,bal,name)
        Coupen.objects.filter(id = id).update(price=val, name=name, remaining=bal)
    return redirect('coupen-manage')


def cpn_dlt(request,id):
    Coupen.objects.filter(id=id).delete()
    return redirect('coupen-manage')