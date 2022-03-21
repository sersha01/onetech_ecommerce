from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SignupCoupon)
admin.site.register(Brand)
admin.site.register(Coupen)
admin.site.register(WishList)