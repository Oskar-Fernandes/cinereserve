from django.db import models
from django.conf import settings


class Ticket(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'reserved', 'Reserved'
        PURCHASED = 'purchased', 'Purchased'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    session = models.ForeignKey('movies.Session', on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey('movies.Seat', on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)
    ticket_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'seat')

    def __str__(self):
        return f"{self.ticket_code} - {self.user.email}"