from django.contrib import admin

from .models import BankUser


class BankUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
	list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
	search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
	ordering = ('username',)


admin.site.register(BankUser, BankUserAdmin)
