from django.contrib import admin
from .models import ProductCategory, Product, Customer, Order, OrderItem, Banner

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Banner)
