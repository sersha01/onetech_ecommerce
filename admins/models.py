from django.db import models
from numpy import product
from users.models import Address, User


# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200, null=True)
    category_off = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    images1 = models.ImageField(upload_to='images/', blank=True)
    images2 = models.ImageField(upload_to='images/', blank=True)
    images3 = models.ImageField(upload_to='images/', blank=True)
    ram = models.CharField(max_length=200, null=True)
    storage = models.CharField(max_length=200, null=True)
    camara = models.CharField(max_length=200, null=True)
    battery = models.CharField(max_length=200, null=True)
    processor = models.CharField(max_length=200, null=True)
    display = models.CharField(max_length=200, null=True)
    stock = models.IntegerField(null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    product_off = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def image1Url(self):
        try:
            url = self.images1.url
        except:
            url = ''
        return url

    @property
    def image2Url(self):
        try:
            url = self.images2.url
        except:
            url = ''
        return url

    @property
    def image3Url(self):
        try:
            url = self.images3.url
        except:
            url = ''
        return url

    @property
    def offer(self):
        if self.product_off != 0 or self.brand.category_off != 0:
            return self.brand.category_off if self.product_off < self.brand.category_off else self.product_off

    @property
    def last_price(self):
        if self.product_off != 0 and self.brand.category_off != 0:
            if self.product_off < self.brand.category_off:
                price = self.price - (self.price * self.brand.category_off / 100)
            else:
                price = self.price - (self.price * self.product_off / 100)
        elif self.product_off != 0:
            price = self.price - (self.price * self.product_off / 100)
        elif self.brand.category_off != 0:
            price = self.price - (self.price * self.brand.category_off / 100)
        else:
            price = self.price
        return price


class SignupCoupon(models.Model):
    TYPE = (('Normal','Normal'),('ReferredTo','ReferredTo'),('ReferredBy','ReferredBy'))
    name = models.CharField(max_length=200, choices = TYPE, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=200, null=True)
    available = models.BooleanField(null=True, default = True)
    proceed = models.BooleanField(null=True, default = False)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (('New','New'),('Pending','Pending'),('Shipped','Shipped'),('Delivered','Delivered'),('Cancelled','Cancelled'),('Return','Return'),('UserCancelled','UserCancelled'))
    METHOD = (('COD','COD'),('PayPal','PayPal'),('RazorPay','RazorPay'))
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True)
    total = models.IntegerField(null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 200,choices = STATUS, default = 'New', null=True)
    order_status = models.BooleanField(null=True,default=False)
    buy_now = models.BooleanField(null=True,default=False)
    payment = models.BooleanField(null=True, default = False)
    payment_method = models.CharField(max_length = 200,choices = METHOD, null=True)
    coupen = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user)
    
    @property 
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        if self.coupen is not None:
            total -= (total * float(self.coupen))/100
        return total
    
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.last_price * self.quantity
        return total

class Banner(models.Model):
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=True)

class Coupen(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200, null=True)
    available = models.BooleanField(null=True, default = True)
    proceed = models.BooleanField(null=True, default = False)
    remaining = models.IntegerField()

class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)