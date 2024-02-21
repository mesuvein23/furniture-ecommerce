from django.shortcuts import render,redirect
from .models import *
from vendor.models import *
from django.views.generic import TemplateView,ListView,UpdateView,DetailView,CreateView
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'customer/home.html')

def contact(request):
    return render(request,'customer/contact.html')

def displaycateg(request):
    cate = Category.objects.all()
    print(cate)
    return render(request,'navbar.html', {'cate':cate})

class store(ListView):
    model = Product
    template_name = 'customer/store.html'

class products_display(DetailView):
    model = Product
    fields = '__all__'
    template_name = 'customer/products_display.html'

def addToCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            action = request.POST.get('action')
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
        return render(request, "customer/cart.html", {'cart':cart, 'total_price':total_price})
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
        return render(request, "customer/checkout.html", {'cart': cart, 'total_price': total_price,'userprofile':userprofile})

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
        return render(request, 'customer/myorders.html', {'c_order':c_order})
    else: 
        messages.warning(request, "Login to continue")
        return redirect('/')


def vieworder(request,t_no):
    order = Order.objects.filter(tracking_no=t_no, user=request.user).first()
    print(order)
    orderitems = OrderItem.objects.filter(order=order)
    print(orderitems)
    return render(request, 'customer/vieworders.html',{'order':order, 'orderitems':orderitems})