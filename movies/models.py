from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    poster_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    columns = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='sessions')
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.datetime}"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    column = models.PositiveIntegerField()

    class Meta:
        unique_together = ('room', 'row', 'column')

    def __str__(self):
        return f"{self.row}{self.column}"