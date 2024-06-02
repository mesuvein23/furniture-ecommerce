from django.urls import path
from . import views


urlpatterns = [
    path('vendor/',views.home.as_view(),name="vendor"),
    path('categorycreate/',views.CategoryAdd,name="category_create"),
    path('categorylist/',views.Category,name="category_list"),
    path('productcreate/',views.ProductCreate.as_view(),name="product_create"),
    path('productdisplay/',views.ProductDisplay.as_view(),name="productdisplay"),

    path('vloginpage/', views.Login.as_view(), name="vendor_login_page"),
    path('vendorlogin/', views.HandleLogin, name="vendorlogin"),
    path('vendorlogput/', views.HandleLogout, name="vendorlogout"),

    path('vendorregister/', views.register, name="vendorregister"),


]