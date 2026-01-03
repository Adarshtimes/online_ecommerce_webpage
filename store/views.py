from django.shortcuts import render,redirect
from django.http import  HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
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


def signup(request):
    if request.method=="GET":
         return render(request,'signup.html')
    
    else:
        postData= request.POST
        name = postData.get('name')
        phone = postData.get('phone')

      
        error_message = None
        value = {
            'name': name,
            'phone': phone
        }

        if not name:
            error_message = "Name is required!"
        elif not phone:
            error_message = "Mobile number is required!"
        elif len(phone) < 10:
            error_message = "Mobile number must be at least 10 digits!"

        elif Customer.objects.filter(phone=phone).exists():  
            error_message = "Mobile Number Already Exists"
        
        if error_message:
            return render(request, 'signup.html', {'error': error_message,'values': value})

        
        try:
            customer = Customer(name=name, phone=phone)
            customer.register()
            return render(request, 'signup.html', {'success': 'Signup successful! You can now login.'})
        except Exception as e:
            return render(request, 'signup.html', {'error': str(e)})