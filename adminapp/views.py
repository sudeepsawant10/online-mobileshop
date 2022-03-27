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
    total_orders = Order.objects.all()
    context = {
        'id':kwargs['id'],
        'total_orders':total_orders,
    }
    return render(request, 'adminapp/total_orders.html', context)

def add_product(request, **kwargs):
    
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
            brands = Brand.objects.all()
            context = {
                'id':kwargs['id'],
                'brands':brands,
                'product_form':product_form,
            }
            context['product_form'] = product_form
            return render(request, 'adminapp/add_product.html',context)
    else:
        product_form = AddProduct()
        brands = Brand.objects.all()
        context = {
            'id':kwargs['id'],
            'brands':brands,
            'product_form':product_form,
        }
        return render(request, 'adminapp/add_product.html',context)


def add_address(request, **kwargs):
    address_form = CreateAddress()
    # user_create = UserCreate(instance=user)
    if request.method == 'POST':
        print("post called")
        address_form = CreateAddress(request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            user = request.user
            address_form.user = user
            address_form.save()
            messages.success(request, 'Address saved')
            print("Address added")
            return redirect('account', id=user.id)
        else:
            context = {
                'id': kwargs['id'],
                'address_form': address_form,
            }
            return render(request, 'customer/address.html', context)
    else:
        context = {
            'id': kwargs['id'],
            'address_form': address_form,
        }
        return render(request, 'customer/address.html', context)


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