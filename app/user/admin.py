from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from user import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'username', 'birthdate', 'image']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'birthdate', 'image')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'image',
                       'username', 'birthdate', 'is_active', 'is_staff')
        }),
    )


admin.site.register(models.User, UserAdmin)
