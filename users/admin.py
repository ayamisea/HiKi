from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            _('Personal info'),
            {
                'fields': (
                    'name',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'verified', 'is_active', 'is_staff', 'is_superuser',
                    'groups', 'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {'fields': ('last_login', 'date_joined')},
        )
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1', 'password2',
                    'name', 'verified',
                ),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
