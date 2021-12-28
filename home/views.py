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
    # context={}
    # for brand in brands:
    #     context[brand] = Product.objects.filter(brand_id=brand.id)
    # # context = {
    # #     # 'products':products,
    # #     'brands': brands,
    # # }
    # print(context)
    # for brand in context:
    #     print("Brand = ", brand)
    #     for product in context.get(brand):
    #         print("Product = ", product)
    #     print("")
    context={
        'brands':brands,
        'products':products,
    }
    return render(request, 'home/index.html', context)

def register(request):
    user_create = UserCreate()
    # dictionary that store User form Structure object data in user_create key
    context = {'user_create': user_create}
    return render(request, 'home/register.html')

def addUser(request):
    user_create = UserCreate(request.POST)
    print("post request")

    # data is filled according to requirements and restirctions then it is valid
    if user_create.is_valid():
        # ready to save temporarily save
        user_create = user_create.save(commit=False)
        # permenent save
        user_create.save()
        # display this message after saving data into user database
        messages.success(request, 'Account created successfully.')
        # go to login url
        return redirect('login')
    else:
        # messages.errors(request, user_create_form.errors)
        # if not valid again take the structure and restriction of form and pass to regitser.html
        context = {'user_create': user_create}

        # add into form
        return render(request, 'home/register.html', context)


class RegisterUser(View):
    # To pass form restrictions or structure to register.html if user comes to register/ url
    def get(self, request):
        # calling normal url page
        # object of UserCreate class
        user_create = UserCreate()
        # dictionary that store User form Structure object data in user_create key
        context = {'user_create': user_create}

        # passing
        return render(request, 'home/register.html', context)
    # when user submit the registeration form
    def post(self, request):
        # request.POST means submit the data in this Model and also store the data in object to check data is valid or not according to UserCreate class restrictions

        #take data filled by user in user_create
        user_create = UserCreate(request.POST)
        
        print("post request")

        # data is filled according to requirements and restirctions then it is valid
        if user_create.is_valid():
            # ready to save temporarily save
            user_create = user_create.save(commit=False)
            # permenent save
            user_create.save()
            # display this message after saving data into user database
            messages.success(request, 'Account created successfully.')
            # go to login url
            return redirect('login')
        else:
            # messages.errors(request, user_create_form.errors)
            # if not valid again take the structure and restriction of form and pass to regitser.html
            context = {'user_create': user_create}

            # add into form
            return render(request, 'home/register.html', context)


class Login(View):
    #when user visit login/ url render this page
    def get(self, request):
        return render(request, 'home/login.html')

    #when user submit the login credentials
    def post(self, request):

        user = authenticate(request, email=request.POST['inputEmail'], password=request.POST['inputPassword'])
        if user:
            login(request, user)
            if user.is_staff:
                
                return redirect("userhome", id = user.id)
                # return redirect('profile')
                # print(user.id)
                # return HttpResponse('<h1>U are Admin</h1>')
            
            #if user is normal then redirect to userhome url with user.id this url will call some views active=>allow to login not banned
            elif user.is_active:
                #id = user.id it will take id of above authenticated username
                # return redirect('index', id=user.id)
                return redirect("userhome", id = user.id)
                # return redirect('profile')
                # print(user.id)
                # return HttpResponse('<h1>U are User</h1>')
                
            #show login page
            else:
                messages.warning(request, 'Invalid email or password.')
                return redirect('login')
         #if user is not authenticated show again login page
        else:
            messages.warning(request, 'Invalid email or password.')
            return redirect('login')



def Logout(request):
    #to logout use this inbuilt function
    logout(request)
    print("logout succussfull")
    #redirect to home
    return redirect('index')