from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.forms import CustomUserCreationForm, CustomUserChangeForm
from app.models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)