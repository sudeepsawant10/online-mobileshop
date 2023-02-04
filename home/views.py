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
    brand_cat = Product.objects.values('brand_id', 'id').order_by('brand_id')
    brand_names=[]
    all_products=[]

    brands = {item['brand_id'] for item in brand_cat}
    for br in brands:
        products = Product.objects.filter(brand_id=br)
        all_products.append(products[:4])
    
    context = {
        'products':products,
        'all_products': all_products[:3],
    }
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
            context = {'user_create': user_create}
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
