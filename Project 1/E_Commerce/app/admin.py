from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *
from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, DeliveryAssignment

# Register your models here.
class Product_Images(admin.TabularInline):
    model = Product_Image

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)
    list_display = ('product_name','price','Categories')
    list_editable = ('Categories','price')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    actions = ['deactivate_users', 'activate_users']

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Selected users deactivated successfully.')

    deactivate_users.short_description = 'Deactivate selected users'

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Selected users activated successfully.')

    activate_users.short_description = 'Activate selected users'


class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ['delivery_man', 'product', 'assigned_date']
    list_filter = ['delivery_man', 'product']
    search_fields = ['delivery_man__username', 'product__product_name']

# admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(slider)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)

# Unregister the default UserAdmin, if needed
admin.site.unregister(User)
# Register the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

#admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAssignment)