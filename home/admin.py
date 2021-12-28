from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name', 'first_name','last_name', 'contact')
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-joinedOn',)
    list_display = ('email', 'user_name', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'contact')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'contact', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'contact', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


# admin.site.register(User)
admin.site.register(User, UserAdminConfig)
# admin.site.register(Product)
# admin.site.register(Order)
