from django.contrib import admin
from .models import Movie, Room, Session, Seat


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration_minutes')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'columns')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'room', 'datetime')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('room', 'row', 'column')