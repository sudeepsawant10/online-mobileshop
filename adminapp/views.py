from django.shortcuts import render, redirect
from customer.models import Product, Order, Brand
from .forms import AddProduct
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def products(request, **kwargs):
    user = request.user
    products = Product.objects.all()
    context = {
        'id':kwargs['id'],
        'products':products,
    }
    return render(request, 'adminapp/products.html',context)

def orders(request, **kwargs):
    total_orders = Order.objects.all().order_by('date')
    context = {
        'id':kwargs['id'],
        'total_orders':total_orders,
    }
    return render(request, 'adminapp/total_orders.html', context)

def add_product(request, **kwargs):
    brands = Brand.objects.all()
    product_form = AddProduct()
    context = {
        'id':kwargs['id'],
        'brands':brands,
        'product_form':product_form
    }

    if request.method == 'POST':
        print("post called product")
        product_form = AddProduct(request.POST, request.FILES)  
        # print(product_form)
        if product_form.is_valid():
            print("product form valid")
            selectedBrand = request.POST.get('selectedBrand')
            brand_instance = Brand.objects.get(pk=selectedBrand)
            print(brand_instance)
            product_form = product_form.save(commit=False)
            product_form.brand_id = brand_instance
            product_form.save()
            messages.success(request, 'New mobile product added')
            print("Product saved")
            return redirect('products', id=kwargs['id'])
        else:
            print("invalid product form")
            product_form = AddProduct()
            return render(request, 'adminapp/add_product.html',context)
    
    return render(request, 'adminapp/add_product.html',context)


def update_status(request, **kwargs):
    total_orders = Order.objects.all()
    context = {
        'id':kwargs['id'],
        'total_orders':total_orders,
    }
    if request.method == 'POST':
        try:
            orderid = request.POST.get('orderid')
            orderStatus = request.POST.get('orderStatus')
            order = Order.objects.get(pk=orderid)
            print(order.status,"----")
            print(orderStatus)
            print(orderid)
            order.status = orderStatus
            print("now", order.status)
            order.save()
            print("order updated")
            total_orders = Order.objects.all()
            messages.success(request, 'Order status updated')
            context['total_orders'] = total_orders
            return render(request, 'adminapp/total_orders.html', context)
        except Exception as e:
            messages.warning(request, 'Please choose order status thent update')
            return render(request, 'adminapp/total_orders.html', context)            
    else:
        return render(request, 'adminapp/total_orders.html', context)