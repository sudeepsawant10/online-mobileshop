from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout, name='logout'),
  
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)