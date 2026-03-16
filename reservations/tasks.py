from celery import shared_task
from django.core.cache import cache


@shared_task
def release_seat_lock(session_id, seat_id):
    lock_key = f"seat_lock:{session_id}:{seat_id}"
    cache.delete(lock_key)
    return f"Lock released for seat {seat_id} in session {session_id}"