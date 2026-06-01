from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Application

admin.site.register(User, UserAdmin)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transport_type', 'start_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'transport_type', 'payment_method')
    search_fields = ('user__username', 'user__fio', 'user__phone')
    readonly_fields = ('created_at',)