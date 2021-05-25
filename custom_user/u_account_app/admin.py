from django.contrib import admin
from .models import MyUser


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'company_name', 'phone', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active']
    list_display_links = ['email', 'company_name']
    search_fields = ['email', 'company_name', 'phone']
    readonly_fields = ['date_joined', 'last_login']
    list_filter = ['last_login']
    list_per_page = 5
    ordering = ['email']


admin.site.register(MyUser, MyUserAdmin)
