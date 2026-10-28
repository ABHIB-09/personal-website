from django.contrib import admin
from .models import ContactMessage
from .models import SocialLink

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'phone', 'company', 'project_type', 'received_at', 'is_read')
    list_filter     = ('project_type', 'is_read', 'received_at')
    search_fields   = ('name', 'email', 'phone', 'company', 'message')
    readonly_fields = ('name', 'email', 'phone', 'company', 'project_type', 'message', 'received_at')
    list_editable   = ('is_read',)
    date_hierarchy  = 'received_at'
    ordering        = ('-received_at',)

    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('project_type', 'message')
        }),
        ('Meta', {
            'fields': ('received_at', 'is_read')
        }),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active']