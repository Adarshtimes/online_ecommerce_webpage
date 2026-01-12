# from urllib import request
from django.shortcuts import render, redirect
from django.http import  HttpResponse
from .models.product import Product
from .models.category import Category
from django.views import View
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail

import uuid

from django.http import JsonResponse
from django.db.models import Q

# from store.models import customer


# from store.models import customer
# Create your views here.


# ============== home function ==================
def home(request):
    totalitem = 0
    if not request.session.has_key('phone'):
        return redirect('login')
    
    phone = request.session['phone']
    customer = Customer.objects.get(phone=phone)
    category = Category.get_all_categories()
    totalitem = len(Cart.objects.filter(phone=phone))
    
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(category_id=categoryID)
    else:
        products = Product.get_all_products()
    
    data = {
        'Product': products,
        'categories': category,
        'name': customer.name,
        'totalitem':totalitem
    }
    
    return render(request, 'home.html', data)



# ====================== product detail function ==================

def productdetail(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem = len(Cart.objects.filter(phone=phone))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer = Customer.objects.filter(phone=phone).first()
        name = customer.name if customer else None

        data = {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'name': name,
            'totalitem': totalitem
        }

        return render(request, 'productdetail.html', data)
    else:
        return redirect('login')  


# ================= logout page =========================

def logout(request):
    if request.session.has_key('phone'):
        del request.session["phone"]
        return redirect('login')
    else:
        return redirect('login')
    
       
def add_to_cart(request):
    phone = request.session['phone']
    product_id = request.GET.get('prod_id')
    product_name  =Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)
    for p in product:
        image=p.image
        price =p.price
        Cart(phone=phone,product=product_name,image=image,price=price).save()
        return redirect(f"/product-detail/{product_id}")

# ============================ signup page

class signup(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
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
        


# ============== login page ==================



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
        return render(request, 'login.html',data)


# ==================Cart page=========================

def show_cart(request):
     totalitem = 0
     if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem = len(Cart.objects.filter(phone=phone))

        customer = Customer.objects.filter(phone=phone).first()
        name = customer.name if customer else None
        cart = Cart.objects.filter(phone=phone)
        data = {
           'name': name,
           'totalitem': totalitem,
            'cart': cart
            }

        if cart:
                return render(request,'show_cart.html',data)
        else:
                return render(request,'empty_cart.html')

def plus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        Product_id = request.GET.get('prod_id')
        cart = Cart.objects.filter(Q(product_id=Product_id) & Q(phone=str(phone))).first()

        if cart:
            cart.quantity += 1
            cart.save()

            data = {
            'quantity': cart.quantity,
            'total_price': cart.quantity * cart.product.price,
            'item_price': cart.product.price
           }

        else:
            data ={
                'quantity':0,
            }
        return JsonResponse(data)
    # ================= minus cart function =========================
def minus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        Product_id = request.GET.get('prod_id')
        cart = Cart.objects.filter(Q(product_id=Product_id) & Q(phone=str(phone))).first()

        if cart:
            cart.quantity -= 1
            cart.save()

            data = {
            'quantity': cart.quantity,
            'total_price': cart.quantity * cart.product.price,
            'item_price': cart.product.price
           }

        else:
            data ={
                'quantity':0,
            }
        return JsonResponse(data)
    
# ================== remove cart function =========================

def remove_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        Product_id = request.GET.get('prod_id')
        cart = Cart.objects.filter(Q(product_id=Product_id) & Q(phone=str(phone))).first()

        if cart:
            cart.delete()
        else:
            data ={
                'quantity':0,
            }
        return JsonResponse(data)
    


# ================ check out fnction ============

def checkout(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        payment_method = request.POST.get('payment_method')
        
        cart_product  = Cart.objects.filter(phone=phone)

        last_order = None

        for c in cart_product:
            last_order = OrderDetail.objects.create(
                user=int(phone),
                product_name=c.product,
                image=c.image,
                qty=c.quantity,
                price=c.price,
                payment_method=payment_method,
                payment_status='PENDING'
            )


        return redirect('upi_payment', order_id=last_order.id)

    else:
        return redirect('login')
    #         OrderDetail(user=phone,product_name=product_name,image=image,qty=qty,price=price).save()
    #     cart_product.delete()

    #     totalitem = len(Cart.objects.filter(phone=phone))
    #     customer = Customer.objects.filter(phone=phone).first()
    #     name = customer.name if customer else None
    #     data ={
    #             'name':name,
    #             'totalitem':totalitem,
    #         }

    #     return render(request,'empty_cart.html',data)

    # else:
    #     return redirect('login')
    

# ================= order page ========================

def order(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem = len(Cart.objects.filter(phone=phone))

        customer = Customer.objects.filter(phone=phone).first()
        name = customer.name if customer else ''

 
        orders = OrderDetail.objects.filter(user=int(phone))
        
            

        data = {
            'orders':orders,
            'name':name,
            'totalitem':totalitem,
        }

            # order = OrderDetail.objects.filter(user=phone)
        if orders:
                return render(request, 'order.html',data)
        else:
                return render(request, 'emptyorder.html',data)

    else:
        return redirect('login')
    

    # ==============search function ==================

def search(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query = request.GET.get('query')

        if not query:
            return redirect('homepage')

        search=Product.objects.filter(name__icontains=query)
        category = Category.get_all_categories()

        totalitem = len(Cart.objects.filter(phone=phone))


        customer = Customer.objects.filter(phone=phone).first()
        name = customer.name if customer else None
        data = {
            'name':name,
            'totalitem':totalitem,
            'categories': category,
            'Product': search,
        }
        return render(request, 'home.html',data)
    else:
        return redirect('login')



# =========upi payment option============
def upi_payment(request, order_id):
    order = OrderDetail.objects.get(id=order_id)

    if request.method == "POST":
        upi_id = request.POST.get('upi_id')

        order.upi_id = upi_id
        order.transaction_id = str(uuid.uuid4())
        order.payment_status = 'SUCCESS'
        order.save()

        return redirect('payment_success')

    return render(request, 'upi_payment.html', {'order': order})


def payment_success(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        Cart.objects.filter(phone=phone).delete()

    return render(request, 'payment_success.html')