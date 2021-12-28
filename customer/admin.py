from django.contrib import admin
from . models import Address, Product, Brand, Payment, Order, Cart, Review
# Register your models here.

@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'flat_no', 'building', 'area', 'city', 'pin']


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['model', 'short_description', 'selling_price', 'discount_price', 'quantity', 'image']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'payment_type', 'card_number', 'amount']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'product_id', 'payment_id', 'quantity', 'date', 'total_amount', 'status']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'item', 'quantity']

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'product', 'stars']