from django.contrib import admin

from .models import ContactMessage, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")
