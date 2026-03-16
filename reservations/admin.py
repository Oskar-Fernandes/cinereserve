from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'user', 'session', 'seat', 'status', 'created_at')
    list_filter = ('status',)