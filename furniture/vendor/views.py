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
# Create your views here.


class home(TemplateView):
    template_name = 'vendor/home.html'

def vendor(request):
    return render(request, 'vendor/admin/index.html') 



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 =request.POST['pass2']
        
    # if pass1!=pass2:
    #         messages.error(request, "Password does not match!!")
    #         return redirect('home')
    # elif not is_valid_password(pass1):
    #     messages.error(request, "Fill the criteria")
    # elif not username.isalnum():
    #     messages.error(request,"Username must be alphanumeric")
    # elif len(username)<3:
    #     messages.error(request,"username should be greater than 3 characters")    
    # else:
        user= User.objects.create_user(username,email, pass1)
        subject = 'welcome to GFG world'
        message = f'Hi {user.username}, thank you for registering in Jayabarahifurniture.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request, "User registered successfully")
        return redirect('home')
    return render(request, '')

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
            messages.danger(request, "Invalid username or password")   

def HandleLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')


def CategoryAdd(request):
    if request.method =='POST':
        name = request.POST['category']
        category_image = request.FILES.Get['image']
        print(name)
        print(category_image)
        allpost = Product.objects.create( 
            name=name,
            image = category_image            )
    return render(request, 'vendor/category/categorycreate.html')

def Category(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, 'vendor/category/categorylist.html', {'categories': categories})

def ProductCreate(request):
    if request.method =='POST':
        pname = request.POST['name']
        print(pname)
        pdescription = request.POST['description']
        pimage = request.FILES['image']
        pslug = request.POST['productslug']
        pm_price = request.POST['m_price']
        ps_price = request.POST['s_price']
        # pnew_arrivals = request.POST['newarrivals']
        # ptop_selling = request.POST['topselling']

        allproduct = Product.objects.create(
            title = pname,
            description = pdescription,
            image = pimage,
            slug = pslug,
            m_price = pm_price,
            s_price = ps_price,
            # new_arrivals = pnew_arrivals,
            # top_selling = ptop_selling
        )
        print(allproduct)
    return render(request, 'vendor/productcreate.html')
        

class ProductDisplay(TemplateView):
    template_name = 'vendor/productdisplay.html'
