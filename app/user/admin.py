from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,GroupAdmin 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Group
from django.utils.translation import gettext, gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['pk', 'email', 'username', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Region'), {'fields': ('municipalities',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','email','municipalities'),
        }),
    )
    filter_horizontal = ('municipalities','groups','user_permissions')