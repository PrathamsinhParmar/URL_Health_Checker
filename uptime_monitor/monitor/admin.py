from django.contrib import admin
from .models import MonitoredURL, CheckLog


@admin.register(MonitoredURL)
class MonitoredURLAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'current_status', 'last_checked', 'is_active', 'user']
    list_filter = ['is_active', 'current_status', 'user']
    search_fields = ['name', 'url', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'last_checked', 'current_status', 'current_response_time']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(CheckLog)
class CheckLogAdmin(admin.ModelAdmin):
    list_display = ['monitored_url', 'timestamp', 'status_code', 'response_time', 'is_up']
    list_filter = ['is_up', 'monitored_url']
    search_fields = ['monitored_url__name', 'monitored_url__url']
    readonly_fields = ['timestamp']
    list_per_page = 50

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('monitored_url', 'monitored_url__user')
