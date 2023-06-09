from django.contrib import admin
from .models import Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'tag', 'operator_code', 'timezone')
    list_display_links = ('id', 'phone_number')
    list_filter = ('tag', 'operator_code', 'timezone')
    search_fields = ('phone_number', 'tag')
    readonly_fields = ('operator_code',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'filter_params', 'start_time', 'end_time', 'sent_count', 'total_count')
    list_display_links = ('id', 'short_text')
    list_filter = ('filter_params',)
    search_fields = ('text', 'filter_params')
    readonly_fields = ('sent_count', 'total_count')

    def short_text(self, obj):
        return f'{obj.text[:50]}...' if len(obj.text) > 50 else obj.text


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'mailing', 'send_time', 'status')
    list_display_links = ('id', 'client', 'mailing')
    list_filter = ('status',)
    search_fields = ('client__phone_number', 'mailing__text')
    readonly_fields = ('send_time', 'status')
