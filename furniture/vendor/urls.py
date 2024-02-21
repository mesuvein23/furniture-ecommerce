from django.urls import path
from . import views


urlpatterns = [
    path('vendorhome/',views.home.as_view(),name="vendorhome"),
    path('categorycreate/',views.CategoryAdd,name="category_create"),
    path('categorylist/',views.Category,name="category_list"),
    path('productcreate/',views.ProductCreate,name="pro"),
    path('productdisplay/',views.ProductDisplay.as_view(),name="productdisplay"),

    path('vloginpage/', views.Login.as_view(), name="vendor_login_page"),
    path('vendorlogin/', views.HandleLogin, name="vendorlogin"),
    path('vendorlogput/', views.HandleLogout, name="vendorlogout"),

    

]