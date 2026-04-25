from django.contrib import admin

from .models import ContactMessage, Event, Officer

admin.site.register(Officer)
admin.site.register(Event)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "submitted_at", "is_resolved")
    list_filter = ("is_resolved", "submitted_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("submitted_at",)
