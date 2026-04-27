from django.contrib import admin

from .models import ContactMessage, Event, GalleryImage, Officer

admin.site.register(Officer)
admin.site.register(Event)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "created_at")
    list_editable = ("display_order",)
    search_fields = ("title", "alt_text")
    readonly_fields = ("created_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "submitted_at", "is_resolved")
    list_filter = ("is_resolved", "submitted_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("submitted_at",)
