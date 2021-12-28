from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from customer.models import Product, Brand
# Create your views here.
def index(request, **kwargs):
    products = Product.objects.all()
    brands = Brand.objects.all()
    print("hellloooo")
    context = {
        'id':kwargs['id'],
        'products':products,
        'brands': brands,
    }
    print(context['products'])
    return render(request, 'customer/index.html', context)

def product_details(request, **kwargs):
    product = Product.objects.get(id=kwargs['pid'])
    user = request.user
   
    if user.is_active:
        context = {
        'id':kwargs['id'],
        'pid':kwargs['pid'],
        'product':product,
        }
        return render(request, "customer/product-details.html", context)
    else:
        context = {
        'id':kwargs['id'],
        'product':product,
        }
        return render(request, "customer/product-details.html", context)
