
from django.contrib import admin
from django.urls import path
# from .views import home
from store import views


urlpatterns = [
    path('', views.home,name='homepage'),
    path('login',views.login.as_view(),name='login'),
    path('product-detail/<int:pk>',views.productdetail,name='product-detail'),
    path('logout',views.logout,name='logout')
]
