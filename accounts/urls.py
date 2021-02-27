from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView , LogoutView

urlpatterns = [
    path('', views.home,name='home'),
    path('accounts/login/',LoginView.as_view(),name='login'),
    path('accounts/logout/',LogoutView.as_view(),name='logout'),
    path('register/', views.registraionPage,name='registraion'),
    path('products/',views.products,name='products'),
    path('create_product/',views.createProduct, name='create_product'),
    path('update_product/<str:pk>',views.updateProduct, name='update_product'),
    path('delete_cproduct/<str:pk>',views.deleteProduct, name='delete_product'),
    path('customer/<str:pk>',views.customer,name='customer'),
    path('create_order/<str:pk>',views.createOrder, name='create_order'),
    path('update_order/<str:pk>',views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>',views.deleteOrder, name='delete_order'),
    path('create_customer/',views.createCustomer, name='create_customer'),
    path('update_customer/<str:pk>',views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>',views.deleteCustomer, name='delete_customer'),
]
