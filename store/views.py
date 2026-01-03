from django.shortcuts import render
from django.http import  HttpResponse
from .models.product import Product
from .models.category import Category
from django.views import View
from django.shortcuts import redirect
from .models import Customer



# Create your views here.

def home(request):
    products = None
    if request.session.has_key('phone'):
        phone = request.session['phone']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
    
            categoryID = request.GET.get('category')
            if categoryID:
                products = Product.get_all_product_by_category_id(categoryID)
        
            else:
                products = products.get_all_products()
    
    
                data= {}
                data['name']=name
                data['Product']= Products
                data['categories']= category
                # print('you are',request.session.get('phone'))
                return render(request,'home.html', data) 
    else:
        return redirect('login')
    
    
    
    
    
# ==================== Login ==========================


def login(request):
    if request.method =='GET':
        return render(request,'login.html')
    else:
        phone = request.POST.get('phone')
        error_message  = None
        value = {
            'phone':phone
        }
        customer = Customer.objects.filter(phone = request.POST["phone"])
        if customer:
            return redirect('homepage')
        else:
            error_message = "Mobile Number is invalid !!"
            data = {
                'error': error_message,
                'value':value
            }
        return render(request, 'login.html',{'error':error_message})



class login(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        phone = request.POST.get('phone')
        error_message = None
        value ={
            'phone':phone
            }
        customer = Customer.objects.filter(phone=request.POST["phone"])
        if customer:
            request.session['phone'] = phone
            return redirect('homepage')
        else:
            error_message = "Mobile Number is Invalid !!"
            data = {
                'error':error_message,
                'value':value 
            }
    





def productdetail(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'productdetail.html',{'product':product})


def logout(request):
    if request.session.has_key('phone'):
        del request.session["phone"]
        return redirect('login')
    else:
        return redirect('login')