from django.shortcuts import render
from django.http import  HttpResponse
from .models.product import Product
from .models.category import Category
# Create your views here.

def home(request):
    Products= Product.get_all_products();
    category= Category.get_all_categories();
    
    data= {}
    data['Product']= Products
    data['categories']= category
    return render(request,'home.html', data) 