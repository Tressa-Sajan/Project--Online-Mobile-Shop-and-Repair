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
 
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


