from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,UpdateView,DetailView,CreateView
from . models import *
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate,login,logout
import json
from vendor.models import *
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
import re
# Create your views here.


class home(TemplateView):
    template_name = 'vendor/home.html'

def vendor(request):
    return render(request, 'vendor/admin/index.html') 

def register(request):
    return render(request, 'vendor/vendorregister.html')

def is_valid_password(password):
            # Password criteria: Minimum length 8, at least one uppercase, one lowercase, one digit
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
            return True
        else:
            return False

def vendorregister(request):
    if request.method == "POST":
        # first_name = request.POST['fname']
        # last_name = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 =request.POST['pass2']
        
    if pass1!=pass2:
            messages.error(request, "Password does not match!!")
            return redirect('home')
    elif not is_valid_password(pass1):
        messages.error(request, "Fill the criteria")
    elif not username.isalnum():
        messages.error(request,"Username must be alphanumeric")
    elif len(username)<3:
        messages.error(request,"username should be greater than 3 characters")    
    else:
        user= User.objects.create_user(username,email, pass1)
        subject = 'Order Placed Successfully'
        message = f'Hi {user.username}, Thank you for registering in Jayabarahifurniture.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request, "User registered successfully")
        return redirect('home')
    return render(request, 'vendor/vendorregister.html')

class Login(TemplateView):
    template_name = 'vendor/vendorlogin.html'

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
            messages.warning(request, "Invalid username or password")   
            return redirect('login')


def HandleLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')


def CategoryAdd(request):
    if request.method =='POST':
        name = request.POST['category_name']
        print(name)
        cate_slug = request.POST['category_slug']
        print(cate_slug)
        c_image = request.POST['category_image']
        print(name)
        allpost = Product.objects.create( 
            name=name,
            slug = cate_slug,
            image = c_image )
    return render(request, 'vendor/category/category_create.html')

def Category(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, 'vendor/category/category_list.html', {'categories': categories})

class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    template_name = "vendor/products/product_create.html"
    success_url = reverse_lazy('vendor/products/product_list')

class ProductDisplay(TemplateView):
    template_name = 'vendor/productdisplay.html'
