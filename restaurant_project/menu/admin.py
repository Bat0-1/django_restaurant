from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Category, Dish, Order, CustomUser



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'vegetarian', 'nuts', 'spiciness')
    list_filter = ('category', 'vegetarian', 'nuts', 'spiciness')
    search_fields = ('name',)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'get_email', 'phone', 'address', 'total_price', 'created_at']
    list_display_links = ['id']
    list_filter = ['created_at']  # Optional
    search_fields = ['user__username', 'user__email', 'address']  # Optional

    @admin.display(ordering='user__username', description='Username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email





@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('id',)
    search_fields = ('email', 'username')

    # Fields shown when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
