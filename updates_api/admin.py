from django.contrib import admin
from django.utils.html import format_html
from .models import AppVersion

@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = (
        'version_name',
        'version_code',
        'file_size_display',
        'is_active',
        'force_update',
        'download_link',
        'created_at'
    )
    list_filter = ('is_active', 'force_update', 'created_at')
    search_fields = ('version_name', 'release_notes')
    ordering = ('-version_code',)

    fieldsets = (
        ('Version Identifiers', {
            'fields': ('version_code', 'version_name')
        }),
        ('Binary Package', {
            'fields': ('apk_file', 'file_size_mb')
        }),
        ('Release Notes & Changelog', {
            'fields': ('release_notes',)
        }),
        ('Rollout Settings', {
            'fields': ('is_active', 'force_update')
        }),
    )

    def file_size_display(self, obj):
        return f"{obj.file_size_mb} MB"
    file_size_display.short_description = "Size"

    def download_link(self, obj):
        if obj.apk_file:
            return format_html('<a href="{}" target="_blank" style="color: #2196F3; font-weight: bold;">Download APK</a>', obj.apk_file.url)
        return "No file"
    download_link.short_description = "APK File"
