from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

# from .forms import CustomUserCreationForm, CustomUserChangeForm
User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'date_joined', 'is_staff', 'post_description']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (None, {"fields": ["post_description"]}),)
    add_fieldsets = auth_admin.UserAdmin.add_fieldsets + (
        (None, {"fields": ["post_description"]}),)
