from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('products/<int:id>/', views.products, name='products'),
    path('total_orders/<int:id>/', views.orders, name='total_orders'),
    path('add_product/<int:id>/', views.add_product, name='add_product'),
    path('remove_product/<int:id>/', views.remove_product, name='remove_product'),
    path('update_order/<int:id>/', views.update_status, name='update-order'),
    path('customers/<int:id>/', views.customers, name='customers'),
    path('remove_customer/<int:id>/', views.remove_customer, name='remove_customer'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)