from django.shortcuts import render, redirect
from customer.models import Product, Order, Brand
from .forms import AddProduct
from django.contrib import messages


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
            # brand = product_form['brand'].value()
            print(selectedBrand)
            brand_instance = Brand.objects.get(pk=int(selectedBrand))
            print(brand_instance)
            product_form.save(commit=False)
            product_form.brand_id=brand_instance
            product_form.save()
            messages.success(request, 'New mobile product added')
            print("Product saved")
            redirect('products', id=kwargs['id'])
        else:
            print("invalid product form")
            product_form = AddProduct()
            return render(request, 'adminapp/add_product.html',context)
    
    return render(request, 'adminapp/add_product.html',context)
"""
def image_request(request):  
    if request.method == 'POST':  
        form = UserImageForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'image_form.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImageForm()  
  
    return render(request, 'image_form.html', {'form': form})
    """