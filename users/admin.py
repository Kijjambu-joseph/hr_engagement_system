from django.contrib import admin

from .models import BankUser
from my_app.admin_site import hr_admin_site


@admin.register(BankUser, site=hr_admin_site)
class BankUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'is_active')
	list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
	search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
	ordering = ('-date_joined',)
	fieldsets = (
		('Account Information', {
			'fields': ('username', 'password', 'email')
		}),
		('Personal Information', {
			'fields': ('first_name', 'last_name', 'employee_id')
		}),
		('Role & Region', {
			'fields': ('role', 'region_cluster', 'branch_name')
		}),
		('Permissions', {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
		}),
		('Important Dates', {
			'fields': ('date_joined', 'last_login'),
			'classes': ('collapse',)
		}),
	)
	readonly_fields = ('date_joined', 'last_login')
	filter_horizontal = ('groups', 'user_permissions')
