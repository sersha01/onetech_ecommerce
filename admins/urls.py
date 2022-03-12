from django.urls import path
from . import views

urlpatterns = [
    path('', views.sup_home, name='sup_home'),
    path('customers', views.customers, name='customers'),
    path('customers_sts', views.customers_sts, name='customer_sts'),
    path('products', views.products, name='products'),
    path('orders', views.orders, name='orders'),
    path('order/<int:id>', views.order, name='order'),
    path('product/<int:id>/', views.product, name='product'),
    path('product/<int:id>/<str:edit>/', views.product, name='product'),
    path('login', views.login, name='login'),
    path('delete', views.delete, name='delete'),
    path('add_product', views.add_product, name='add_product'),
    path('sup_logout', views.sup_logout, name='sup_logout'),
    path('order_update', views.order_update, name='order_update'),
    path('get_data', views.get_data, name='get_data'),
    path('sales', views.sales, name='sales'),
    path('test', views.test, name='test'),
    path('copy/<str:id>', views.copy, name='copy'),
    path('test1', views.test1, name='test1'),
    path('exel', views.exel, name='exel'),
    path('csv', views.exportCsv, name='csv'),
    path('coupens', views.coupens, name='coupens'),
    path('offers', views.offers, name='offers'),
]