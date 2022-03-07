from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('<int:id>', views.index, name='userhome'),
    path('search/<int:id>/', views.search, name='search'),
    path('add-to-cart/<int:id>/<int:pid>/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('account/<int:id>/', views.account, name='account'),
    path('address/<int:id>/', views.add_address, name='address'),
    path('product-details/<int:id>/<int:pid>', views.product_details, name='userproduct-details'),
    path('checkout/<int:id>/', views.checkout, name='checkout'),
    path('do_payment/<int:id>/<int:addr_id>/', views.do_payment, name='do_payment'),
    # path('pay/<int:id>/<int:id>', views.pay, name='pay'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('orders/<int:id>/', views.orders, name='orders'),

    
  
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)