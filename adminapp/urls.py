from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('products/<int:id>/', views.products, name='products'),
    path('total_orders/<int:id>/', views.orders, name='total_orders'),
    path('add_product/<int:id>/', views.add_product, name='add_product'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)