"""
URL configuration for E_Commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),

    path('',views.HOME,name='home'),
    path('logout/', views.logoutUser, name='logout'),
  
    path('account/login/',views.LOGIN,name='login'),
    path('account/register/',views.REGISTER,name='handleregister'),
    path('account/login/',views.LOGIN,name='handlelogin'),

    # path('accounts/', include('django.contrib.auth.urls')),
    
    # URL For Admin Dash Board
    path('adminDash/', views.admin_DashBoard_View, name='adminDash'),

    path('profileSettings/', views.profileSettings, name='profileSettings'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('seller_page/', views.seller_page, name='seller_page'),
    path('deactivate/',views.deactivate, name='deactivate'),
    path('activate/',views.activate, name='activate'),

    path('products/', views.productView, name='products'),
    path('category/', views.category, name='category'),
    path('productViewC/', views.productViewC, name='productViewC'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
 
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('create-order/', views.create_order, name='create-order'),
    path('handle-payment/', views.handle_payment, name='handle-payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('bill_invoice/',views.bill_invoice, name='bill_invoice'),

    path('admin_create_delivery_man/', views.admin_create_delivery_man, name='admin_create_delivery_man'),
    path('assign-delivery/', views.assign_delivery, name='assign_delivery'),
    path('admin_Order/',views.admin_Order, name='admin_Order'),

    path('upload_image/',views.upload_image, name='upload_image'),
    path('upload/success/<int:image_id>/', views.upload_success, name='upload_success'),  # Add the URL pattern for upload_success
    path('image/<int:image_id>/', views.view_image, name='view_image'),
# end il ith add cheyyanam



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
