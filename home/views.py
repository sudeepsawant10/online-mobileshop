from django.shortcuts import render
from django.views import View
from .forms import UserCreate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy
from customer.models import Product, Brand



# Create your views here.
def index(request):
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
        'products':products,
        'all_products':all_products,
        'brand_names': brand_names,
    }
    # print(context['products'])
    return render(request, 'home/index.html', context)

def register(request):

    if request.method == 'POST':
        user_create = UserCreate(request.POST)
        # save the data into db
        if user_create.is_valid():
            user_create = user_create.save(commit=False)
            user_create.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            # messages.errors(request, user_create_form.errors)
            context = {'user_create': user_create}
            # add into form
            return render(request, 'home/register.html', context)
    user_create = UserCreate()
    context={
        'user_create':user_create,
    }
    
    return render(request, 'home/register.html', context)

def Login(request):
    
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['inputEmail'], password= request.POST['inputPassword'])
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('total_orders', id=user.id)
            elif user.is_active:
                return redirect('userhome', id=user.id)
            else:
                messages.warning(request, "Invalid email or password")
                return redirect('login')
        else:
            messages.warning(request, "Enter login credentials")
            return redirect('login')
                
    return render(request, "home/login.html")
            

def Logout(request):
    #to logout use this inbuilt function
    logout(request)
    print("logout succussfull")
    #redirect to home
    return redirect('index')
