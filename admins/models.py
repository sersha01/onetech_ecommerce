from django.db import models
from users.models import Address, User


# Create your models here.
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
    brand = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

class Order(models.Model):
    STATUS = (('New','New'),('Pending','Pending'),('Shipped','Shipped'),('Delivered','Delivered'),('Cancelled','Cancelled'),('UserCancelled','UserCancelled'))
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 200,choices = STATUS, default = 'New', null=True)
    order_status = models.BooleanField(null=True,default=False)
    payment = models.BooleanField(null=True, default = False)

    def __str__(self):
        return str(self.user)
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
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
        total = self.product.price * self.quantity
        return total

