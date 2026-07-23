from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from .models import BankUser
from my_app.admin_site import hr_admin_site


@admin.register(BankUser, site=hr_admin_site)
class BankUserAdmin(UserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	model = BankUser
	list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'is_active')
	list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
	search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
	ordering = ('-date_joined',)
	filter_horizontal = ('groups', 'user_permissions')
	readonly_fields = ('date_joined', 'last_login')
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
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'role', 'region_cluster', 'branch_name', 'first_name', 'last_name', 'employee_id', 'groups', 'is_staff', 'is_superuser', 'is_active'),
		}),
	)


@admin.register(Group, site=hr_admin_site)
class GroupAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	filter_horizontal = ('permissions',)
