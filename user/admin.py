from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Book, Trade


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Informações Pessoais', {'fields': ('full_name', 'email')}),
		('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'full_name', 'password1', 'password2')
		}),
	)
	list_display = ('id', 'username', 'email', 'full_name', 'is_staff')
	search_fields = ('username', 'email', 'full_name')
	ordering = ('id',)


admin.site.register(Book)
admin.site.register(Trade)