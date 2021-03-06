from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .forms import SignUpForm
from .models import User


class UserAdmin(DjangoUserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ['email', 'generation', 'gender', 'is_superuser']
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'password',
        )}),
        ('개인정보', {'fields': (
            'generation',
            'gender',

        )}),
        ('권한', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('중요 일자', {'fields': (
            'last_login',
            'date_joined'
        )}),
    )


admin.site.register(User, UserAdmin)
