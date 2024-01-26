from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ['username', 'email', 'display_name', 'first_name',
                    'last_name', 'is_superuser']

    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Extra info', {'fields': ('display_name',)}),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Extra info', {'fields': ('display_name',)}),
    )