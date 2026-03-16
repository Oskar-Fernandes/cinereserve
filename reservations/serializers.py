from rest_framework import serializers
from .models import Ticket
from movies.serializers import SessionSerializer, SeatSerializer


class TicketSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'ticket_code', 'session', 'seat', 'status', 'created_at')