from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from customer.models import Product, Brand, Cart, Address, Order, Payment, Review
from home.forms import UserCreate
from . forms import CreateAddress, PaymentForm, AddReview
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.


def index(request, **kwargs):
    user = request.user
    brand_cat = Product.objects.values('brand_id', 'id').order_by('brand_id')
    all_products = []
    # set of all brands
    brands = {item['brand_id'] for item in brand_cat}

    # Adding each brand 4 products into list
    for br in brands:
        products = Product.objects.filter(brand_id=br)
        all_products.append(products[:4])

    context = {
        'id': kwargs['id'],
        'all_products': all_products[:3],
    }
    return render(request, 'customer/index.html', context)


def search(request, **kwargs):
    query = request.GET['search']
    # products = Product.objects.all()
    # django icontains=> way to query on table
    if len(query) > 80:
        products = Product.objects.none()
    else:
        query_lookup = (Q(model__icontains=query) | Q(short_description__icontains=query))
        get_products = Product.objects.filter(query_lookup)
        # get_description = Product.objects.filter(short_description__icontains=query)
        get_brand = Product.objects.filter(brand_id__name__icontains=query)
        products = get_products.union(get_brand)
        # products = products2.union(get_brand)
        print(products)

    context = {
        'id': kwargs['id'],
        'products': products,
        'query': query,
    }
    return render(request, 'customer/search.html', context)


def product_details(request, **kwargs):
    product = Product.objects.get(id=kwargs['pid'])
    product_match_for_review = False
    order_for_review = 0
    reviews = Review.objects.filter(product_id=product)
    # print(reviews)
    add_review = AddReview()
    pid = product.id
    user = request.user
    if user.is_active:
        myorders = Order.objects.filter(Q(user_id=user) & Q(status='Delivered')).values('id','product_id')
        print("my orders = ", end=" ")
        for mo in myorders:
            if pid == mo['product_id']:
                print("product matched for review")
                product_match_for_review = True
                order_for_review = mo['id']
        print(product_match_for_review)
        print(order_for_review)

        context = {
            'id': kwargs['id'],
            'pid': kwargs['pid'],
            'product': product,
            'product_match_for_review':product_match_for_review,
            'add_review':add_review,
            'reviews':reviews
        }
        if request.method == 'POST':
            print("post called")
            add_review = AddReview(request.POST)
            if add_review.is_valid():
                print("valid form review")
                add_review = add_review.save(commit=False)
                order_instance = Order.objects.get(pk=order_for_review)
                add_review.user_id = order_instance.user_id
                add_review.order_id = order_instance
                add_review.product_id = order_instance.product_id
                add_review.save()
                messages.success(request, 'Review added successfully')
                return render(request, "customer/product-details.html", context)
            else:
                print("Invalid form")
                context['add_review']=add_review
                return render(request, "customer/product-details.html", context)
        else:
            return render(request, "customer/product-details.html", context)
    else:
        context = {
            'id': kwargs['id'],
            'product': product,
            'reviews':reviews,
        }
        return render(request, "customer/product-details.html", context)
    


def add_to_cart(request, **kwargs):
    user = request.user
    product_id = kwargs['pid']
    product = Product.objects.get(id=product_id)
    context = {
        'id': kwargs['id'],
        'pid': kwargs['pid'],
    }
    Cart(user_id=user, product_id=product, quantity=1).save()
    return redirect('cart', id=kwargs['id'])

def cart(request, **kwargs):
    if request.user.is_authenticated:
        user = request.user
        cartItems = Cart.objects.filter(user_id=user)
        cart_product = [p for p in Cart.objects.all() if p.user_id == user]
        print(cart_product)
        context = {
            'id': kwargs['id'],
            'cartItems': cartItems,
        }
        if cart_product:
            context.update(price_detail(user))
            print(context, 'returned..')
            return render(request, 'customer/cart.html', context)
        else:
            return render(request, 'customer/empty_cart.html', context)


def price_detail(user):
    amount = 0.0
    delivery_charges = 40.0
    total_amount = 0.0
    price_data = {}
    # take the all rows of cart for logged in user
    cart_product = [p for p in Cart.objects.all() if p.user_id == user]
    print(len(cart_product))
    # calculate amount according to quantity
    
    for p in cart_product:
        temp_amount = (p.quantity * p.product_id.discount_price)
        amount = amount + temp_amount

    cart_list = list(cart_product)
    print(len(cart_list))
    if amount < 50000:
        if len(cart_product) > 1:
            delivery_charges = 00.0
        total_amount = amount + delivery_charges
        price_data['delivery_charges'] = delivery_charges
    else:
        delivery_charges = 00.0
        total_amount = amount + delivery_charges
        price_data['delivery_charges'] = delivery_charges
    price_data['amount'] = amount
    price_data['total_amount'] = total_amount
    # print(price_data)
    return price_data


def account(request, **kwargs):
    user = request.user
    address = Address.objects.filter(user_id=user)
    # user_create = UserCreate(instance=user)
    context = {
        'id': kwargs['id'],
        'address': address,
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
            address_form.user_id = user
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


def plus_cart(request):
    print("plus clicked")
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        user = request.user
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user_id=request.user))
        c.quantity += 1
        c.save()
        data = {
            'quantity': c.quantity,
        }
        data.update(price_detail(user))
        return JsonResponse(data)


def minus_cart(request):
    print("minus clicked")

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        user = request.user
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user_id=request.user))
        c.quantity -= 1
        c.save()

        data = {
            'quantity': c.quantity,
        }
        data.update(price_detail(user))
        # print(data,'MinusCart data...')
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        user = request.user
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user_id=request.user))
        c.delete()
        data = {}
        data.update(price_detail(user))
        cart_products = list(Cart.objects.filter(user_id=user))
        if(len(cart_products)==0):
            return redirect('cart', id=user.id)
        else:
            print(data)
            print(len(cart_products))
            return JsonResponse(data)


def checkout(request, **kwargs):
    user = request.user
    # payment_form = PaymentForm()
    cart_items = Cart.objects.filter(user_id=user)
    addresses = Address.objects.filter(user_id=user)
    cart_product = [p for p in Cart.objects.all() if p.user_id == user]

    context = {
        'id': kwargs['id'],
        'addresses': addresses,
    }
    if cart_product:
        context.update(price_detail(user))

    return render(request, 'customer/checkout.html', context)


def payment(request, **kwargs):
    user = request.user
    custid = request.POST.get('custid')
    payment_form = PaymentForm()
    context = {
        'id': kwargs['id'],
        'addr_id': custid,
        'payment_form': payment_form,
    }
    try:
        address = Address.objects.get(id=custid)
    except (BaseException )as e:
        print("exception in")
        context['addr_id'] = custid
        messages.info(request, 'Please select or add your address in account')
        return redirect('checkout', id=user.id)
    cart = Cart.objects.filter(user_id=user)
    context['addr_id']=custid
    cart_product = [p for p in Cart.objects.all() if p.user_id == request.user]
    print("payment")
    if cart_product:
        context.update(price_detail(user))
    return render(request, 'customer/payment.html', context)


def do_payment(request, **kwargs):
    user = request.user
    custid = kwargs['addr_id']
    print("payment method called")
    context = {
        'id': kwargs['id'],
        'addr_id': kwargs['addr_id'],
    }
    context.update(price_detail(user))
    cart_items = Cart.objects.filter(user_id=user)
    try:
        address = Address.objects.get(id=custid)
    except Exception as e:
        return redirect('checkout', id=user.id)
    cart_product = [p for p in Cart.objects.all() if p.user_id == request.user]
    if cart_product:
        context.update(price_detail(user))

    payments = (
        ('COD'),
        ('Credit/Debit Card'),
    )

    if request.method == 'POST':
        input_value = request.POST.get('billingOptions')
        if input_value == 'card-payment':
            payment_form = PaymentForm(request.POST)
            print("correct")
            if payment_form.is_valid():
                print("valid")
                payment_form = payment_form.save(commit=False)
                payment_form.user_id = request.user
                payment_form.payment_type = payments[1]
                payment_form.amount = context['total_amount']
                payment_form.save()
                print("payment success")
                if len(cart_items) > 1:
                    for c in cart_items:
                        Order(user_id=user, product_id=c.product_id, payment_id=payment_form, address_id=address,
                            quantity=c.quantity, date=timezone.now(), total_amount=(c.quantity * c.product_id.discount_price)).save()
                        c.delete()
                        print("Placed order")
                else:
                    for c in cart_items:
                        Order(user_id=user, product_id=c.product_id, payment_id=payment_form, address_id=address,
                            quantity=c.quantity, date=timezone.now(), total_amount=context['total_amount']).save()
                        c.delete()
                        print("Placed order")
                messages.success(
                    request, 'Payment successfull and order placed')
                print("placed orders...")
                return redirect('orders', id=user.id)
                # return render(request, 'customer/orders.html', context)
            else:
                # payment_form = PaymentForm()
                print("payment Failed")
                context['payment_form']=payment_form
                return render(request, 'customer/payment.html', context)
        elif input_value == 'cod-order':
            pay = Payment()
            pay.user_id = request.user
            pay.payment_type = payments[0]
            pay.amount = context['total_amount']
            pay.save()
            
            if len(cart_items) > 1:
                for c in cart_items:
                    total_amount = c.quantity * c.product_id.discount_price
                    print(total_amount)
                    if total_amount <50000:
                        total_amount= total_amount + 40
                    Order(user_id=user, product_id=c.product_id, payment_id=pay, address_id=address,
                        quantity=c.quantity, date=timezone.now(), total_amount=(c.quantity * c.product_id.discount_price)).save()
                    c.delete()
                    print("Placed order")
            else:
                for c in cart_items:
                    total_amount = c.quantity * c.product_id.discount_price
                    print(total_amount)
                    if total_amount <50000:
                        total_amount= total_amount + 40
                    Order(user_id=user, product_id=c.product_id, payment_id=pay, address_id=address,
                        quantity=c.quantity, date=timezone.now(), total_amount=context['total_amount']).save()
                    c.delete()
                    print("Placed order")
            messages.success(request, 'Order placed successfully.')
            print("placed orders...")
            return redirect('orders', id=user.id)
            # return HttpResponse("cod")
        else:
            messages.warning(request, 'Please select payment method')
            return render(request, 'customer/payment.html', context)
    else:
        payment_form = PaymentForm()
        context = {
            "payment_form": payment_form,
        }
        return render(request, 'customer/payment.html', context)


def orders(request, **kwargs):
    orders = Order.objects.filter(user_id=request.user)
    user = request.user
    context = {
        'id': kwargs['id'],
        'orders': orders,
    }
   
    return render(request, 'customer/orders.html', context)

def cancel_order(request, **kwargs):
    orders = Order.objects.filter(user_id=request.user)
    context = {
        'id':kwargs['id'],
        'orders':orders
    }
    if request.method == 'POST':
        orderid = request.POST.get('orderid')
        print(orderid)
        status = 'Cancelled'
        order_instance = Order.objects.get(pk=orderid)
        order_instance.status = status
        order_instance.save()
        print("order cancelled")
        messages.info(request, "Order cancelled successfully")
        return render(request, 'customer/orders.html', context)
    else:
        return render(request, 'customer/orders.html', context)
