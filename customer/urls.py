from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('<int:id>', views.index, name='userhome'),
    path('product-details/<int:id>/<int:pid>', views.product_details, name='userproduct-details'),
    
  
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)