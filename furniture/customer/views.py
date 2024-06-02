from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from vendor.models import *
from django.views.generic import TemplateView,ListView,UpdateView,DetailView,CreateView
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
import json
from django.contrib import messages
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def home(request):
    cate = Category.objects.all()
    newarrivals = Product.objects.filter(new_arrivals=True)
    featured_products = Product.objects.filter(top_selling=True)
    return render(request, 'customer/home.html', {'cate':cate, 'newarrivals':newarrivals, 'featured_products':featured_products})

def contact(request):
    if request.method == "POST":
        fname = request.POST['first-name']
        print(fname)
        lname = request.POST['last-name']
        print(lname)
        email = request.POST['email']
        print(email)
        phone = request.POST['phone-number']
        print(phone)
        message = request.POST['message']
        print(message)

        data = Contact.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            message=message,
        )
        messages.success(request, "succesfully submited")
    return render(request, 'customer/contact.html')

def navbar(request):
    return render(request, 'customer/navbar.html')

# def displaycateg(request):
#     print(cate)
#     return render(request,'navbar.html',)

class store(ListView):
    model = Product
    template_name = 'customer/products/store.html'

class show_category(ListView):
    model = Category
    template_name = 'customer/categories/display_categories.html'


class products_display(DetailView):
    model = Product
    fields = '__all__'
    template_name = 'customer/products/show_product.html'
    
class categories_display(DetailView):
    model = Category
    fields = '__all__'
    template_name = 'customer/categories/display_categories.html'



def category_item(request, slug):
    if (Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        print(products)
        category_name = Category.objects.filter(slug=slug).first()
        print(category_name)
        return render(request, 'customer/categories/category.html', { 'products': products , 'category_name' : category_name})
    else:
        messages.warning(request, "No such category found")
        return redirect('/category_item')

def customerlogin(request):
    return render(request, 'customer/auth/login.html')    

def HandleLogin(request):
    if request.method == "POST":
        login_user =request.POST['loginuser']
        login_password = request.POST['loginpassword']

        user =authenticate(request,username=login_user,password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")   
            return redirect('home')
        else:
            messages.danger(request, "Invalid username or password")   

def HandleLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')

def register(request):
    if request.method == "POST":
        try:
            error_list, name ,address, phone = reg_validation(request, None)
            if error_list:
                error_message = {"error": error_list}
                return JsonResponse(error_message, status =404)
            else:
                username = request.POST['username']
                # fname = request.POST['fname']
                # lname = request.POST['lname']
                email = request.POST['email']
                pass1 = request.POST['pass1']
                pass2 =request.POST['pass2']
                user= User.objects.create_user(username,email, pass1)
                subject = 'welcome to GFG world'
                message = f'Hi {user.username}, thank you for registering in Jayabarahifurniture.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request, "User registered successfully")
                return redirect('home')
        
        except Exception as exe:
            print(exe)
            error_message = {"errors": error_list}
            return JsonResponse(error_message, status= 404)
        
    return render(request, 'customer/auth/register.html')


def addToCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            # action = request.POST.get('action')
            cart_qty = request.POST.get('cart_quantity')
            
            try:
                product_check = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': "No such product found"})

            if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                return JsonResponse({'status': "Product Already in Cart"})
            else:
                if int(product_check.quantity) >= int(cart_qty):
                    Cart.objects.create(user=request.user, product_id=prod_id, cart_quantity=cart_qty)
                    return JsonResponse({'status': "Product Added Successfully"})
                else:
                    return JsonResponse({'status': f"Only {product_check.quantity} quantity available"})
        else:
            return JsonResponse({'status': "Login to continue"})

    return redirect('/')

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price =0
        for item in cart:
            total_price = total_price + item.product.selling_price * item.cart_quantity
        return render(request, "customer/cart/cart.html", {'cart':cart, 'total_price':total_price})
    else:
        messages.warning(request, "Login to continue")
        return redirect('/vloginpage')
    
def offcart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price =0
        for item in cart:
            total_price = total_price + item.product.selling_price * item.cart_quantity
        return render(request, "customer/cart/offcanvas.html", {'cart':cart, 'total_price':total_price})
    else:
        messages.warning(request, "Login to continue")
        return redirect('/vloginpage')

def updateItem(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if(Cart.objects.filter(user=request.user, product_id=product_id)):
            cart_qty = request.POST.get('cart_quantity')
            cart = Cart.objects.get(product_id=product_id, user=request.user)
            cart.cart_quantity = cart_qty
            cart.save()
            return JsonResponse({'status': "Updated successfullly"})
    return redirect('/')

def deleteItem(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if(Cart.objects.filter(user=request.user, product_id=product_id)):
            cartitem = Cart.objects.get(product_id=product_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status':"Deleted Successfully"})
    return redirect('/')        

def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.cart_quantity for item in cart)

        userprofile = Profile.objects.filter(user=request.user).first()
        return render(request, "customer/cart/checkout.html", {'cart': cart, 'total_price': total_price,'userprofile':userprofile})

    else:
        messages.warning(request, "Login to continue")
        return redirect('/')
    
def placeorder(request):
    if request.method == 'POST':

        currentuser = request.user

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname') 
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.zipcode = request.POST.get('zipcode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.zipcode = request.POST.get('zipcode')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.cart_quantity
        
        neworder.total_price = cart_total_price
        trackno = 'JB'+ str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'sharma'+ str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno
        neworder.save()

        user=request.user
        subject = 'welcome to GFG world'
        message = f'Hi {OrderItem.product}, Your order has been placed successfully.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.cart_quantity
            )

            # To decrease the product quantity form available stock 
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.cart_quantity
            orderproduct.save()
        # To clear cart's usercart()
        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has bedd placed sucessfully")
             
    return redirect('/')


def orders(request):
    if request.user.is_authenticated:
        c_order = Order.objects.filter(user=request.user)
        return render(request, 'customer/orders/myorders.html', {'c_order':c_order})
    else: 
        messages.warning(request, "Login to continue")
        return redirect('/')


def vieworder(request,t_no):
    order = Order.objects.filter(tracking_no=t_no, user=request.user).first()
    print(order)
    orderitems = OrderItem.objects.filter(order=order)
    print(orderitems)
    return render(request, 'customer/orders/vieworders.html',{'order':order, 'orderitems':orderitems})