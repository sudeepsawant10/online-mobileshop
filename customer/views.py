from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from customer.models import Product, Brand, Cart, Address
from home.forms import UserCreate
from . forms import CreateAddress

# Create your views here.
def index(request, **kwargs):
    products = Product.objects.all()
    brands = Brand.objects.all()
    brand_cat = Product.objects.values('brand_id', 'id')
    brand_names=[]
    all_products=[]

    cat_list = {item['brand_id'] for item in brand_cat}
    print(cat_list)
    for cat in cat_list:
        prod = Product.objects.filter(brand_id=cat)
        all_products.append(prod[:4])
    product_list=[]

    
    for item in brands:
    #     prod = Product.objects.filter(brand_id__name=item.name)
        brand_names.append(item.name)
    # print(all_products)
    # custome_search(request)
    context = {
        'id':kwargs['id'],
        'products':products,
        'all_products':all_products,
        'brand_names': brand_names,
    }
    # print(context['products'])
    return render(request, 'customer/index.html', context)

def search(request, **kwargs):
    query = request.GET['search']
    # products = Product.objects.all()
    # django icontains=> way to query on table
    

    if len(query) > 80:
        products=Product.objects.none()
    else: 
        query_lookup = (Q(model__icontains=query) | Q(short_description__icontains=query))
        get_products = Product.objects.filter(query_lookup)
        # get_description = Product.objects.filter(short_description__icontains=query)
        get_brand = Product.objects.filter(brand_id__name__icontains=query)
        products = get_products.union(get_brand)
        # products = products2.union(get_brand)
        print(products)


    if products.count == 0:
        messages.error("No search results found. Please refine your query")
    
    context = {
        'id':kwargs['id'],
        'products':products,
        'query':query,
    }
    return render(request, 'customer/search.html', context)

def custome_search(request):
    query = request.GET.get('search')
    allprods = []
    allproducts = Product.objects.all()
    brands={product.brand_id.name for product in allproducts}
    products = [item for item in allproducts if query in item.model.lower() or query in item.short_description.lower() or query in item.brand_id.name ]
    # brandsof = [item['brand_id'].name for item in allproducts]
    # print(brandsof)
    # brand_products=Product.objects.values('brand_id','id')
    # # set value
    # cats = {item['brand_id'] for item in brand_products}
    # # print(cats)
    # for cat in cats:
    #     prodtemp = Product.objects.filter(brand_id=cat)
    #     print(prodtemp)
    #     prod = [item for item in prodtemp if searchMatch(query, item)]
    #     allprods.append(prod)
    # print(allproducts[0])
    # print(allproducts[0].brand_id.name)
    # for product in allproducts:
    #     brands.append(product.brand_id.name)
    print(products)
    # print(brands)
    context = {
        # 'products':allprods,
        'query':query,
    }
    return render(request, 'customer/search.html', context)


def searchMatch(query,item):
    # print(query)
    print(item)
    if query.lower() in item.model.lower() or query in item.short_description.lower() or query in str(item.discount_price):
        return True
    else:
        return False

def customSearch(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    cats = {item['name'] for item in brands}
    print("hellloooo")
    context = {
        'id':kwargs['id'],
        'products':products,
        'brands': brands,
    }
    # print(context['products'])
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


def add_to_cart(request, **kwargs):
    # we have to save data using prod_id
    
    user = request.user
    product_id = kwargs['pid']
    product = Product.objects.get(id=product_id)
    # print("*************",product_id)
    Cart
    context = {
        'id':kwargs['id'],
        'pid':kwargs['pid'],
    }
    Cart(user=user, product=product, item=1, quantity=1).save()
    return redirect('cart', id=kwargs['id'])

def cart(request, **kwargs):
    if request.user.is_authenticated:
        user = request.user
        cartItems = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount=40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        context = {
            'id':kwargs['id'],
            'cartItems':cartItems,
           
        }
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discount_price)
                amount+=tempamount
                total_amount = amount + shipping_amount
            print(tempamount)
            print(amount)
            print(total_amount)
            context['total_amount']=total_amount
            context['amount']=amount
            return render(request, 'customer/cart.html',context)
        else:
            return render(request, 'customer/cart.html',context)

def account(request, **kwargs):
    user = request.user
    address = Address.objects.filter(user=user)
    # user_create = UserCreate(instance=user)
    context={
        'id':kwargs['id'],
        'address':address,
        # 'user_create':user_create,
    }
    return render(request, 'customer/account.html', context)

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
            context={
                'id': kwargs['id'],
                'address_form':address_form,
            }
            return render(request, 'customer/address.html',context)
    else:
        context={
                'id': kwargs['id'],
                'address_form':address_form,
        }
        return render(request, 'customer/address.html',context)



def plus_cart(request):
    print("plus clicked")
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()

        amount = 0.0
        shipping_amount=40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount+=tempamount

        data = {
            'quantity':c.quantity,
            'amount': amount,
            'total_amount':amount + shipping_amount,

        }
        print(tempamount)
        print(amount)
        print(total_amount)
        return JsonResponse(data)

def minus_cart(request):
    print("minus clicked")

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        # saving in db
        c.save()

        amount = 0.0
        shipping_amount=40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount+=tempamount

        data = {
            'quantity':c.quantity,
            'amount': amount,
            'total_amount':amount + shipping_amount,

        }
        print(tempamount)
        print(amount)
        print(total_amount)
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # c.quantity-=1
        # saving in db
        c.delete()

        amount = 0.0
        shipping_amount=40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount+=tempamount

        data = {
            'amount': amount,
            'total_amount':amount + shipping_amount,

        }
        print(tempamount)
        print(amount)
        print(total_amount)
        return JsonResponse(data)


