from django.shortcuts import render
from django.http import  HttpResponse
from .models.product import Product
from .models.category import Category
# Create your views here.

def home(request):
    Products= None
    category= Category.get_all_categories();
    
    categoryID= request.GET.get('category')
    if categoryID:
        Products= Product.get_all_products_by_categoryid(categoryID)
    else:
        Products= Product.get_all_products()


    data= {}
    data['Product']= Products
    data['categories']= category
    return render(request,'home.html', data) 