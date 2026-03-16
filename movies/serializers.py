from rest_framework import serializers
from .models import Movie, Session, Seat, Room
from django.core.cache import cache


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = Session
        fields = ('id', 'movie', 'movie_id', 'room', 'datetime', 'created_at')


class SeatSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ('id', 'row', 'column', 'status')

    def get_status(self, obj):
        session_id = self.context.get('session_id')
        if not session_id:
            return 'available'
        from reservations.models import Ticket
        lock_key = f"seat_lock:{session_id}:{obj.id}"
        if cache.get(lock_key):
            return 'reserved'
        if Ticket.objects.filter(session_id=session_id, seat=obj, status='purchased').exists():
            return 'purchased'
        return 'available'
