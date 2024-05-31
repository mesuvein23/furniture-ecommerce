from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('store/', views.store.as_view(), name="store"),
	path('products_display/<str:slug>', views.products_display.as_view(), name="products_display"),
    
	path('category/', views.show_category.as_view(), name="category"),
	path('category_item/<str:slug>', views.category_item, name="category_item"),
    
	# path('categories_display/<int:pk>', views.categories_display.as_view(), name="categories_display"),
	# path('display_category_item/<str:slug>', views.display_category_item, name="display_category_item")
    
	path('contact/', views.contact, name="contact"),
    
	path('login/', views.customerlogin, name="login"),
	path('register/', views.register, name="register"),
    
	path('offcart/', views.offcart, name="ofcart"),


	path('add-to-cart/', views.addToCart, name="add-to-cart"),
	path('cart/', views.cart, name="cart"),
	path('update_item/', views.updateItem, name="update_item"),
	path('delete-cart-item/', views.deleteItem, name="delete-cart-item"),
    
	path('checkout/', views.checkout, name="checkout"),
    path('placeorder',views.placeorder, name="placeorder"),

	path('my-orders', views.orders, name="myorders"),
	path('view-order/<str:t_no>',views.vieworder, name="orderview")
    
    
]