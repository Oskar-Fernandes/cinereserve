from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def release_seat_lock(session_id, seat_id):
    lock_key = f"seat_lock:{session_id}:{seat_id}"
    cache.delete(lock_key)
    return f"Lock released for seat {seat_id} in session {session_id}"


@shared_task
def send_ticket_confirmation_email(user_email, ticket_code, movie_title, session_datetime, seat_row, seat_column):
    subject = 'Confirmação de Ingresso - CineReserve'
    message = f"""
Olá! Seu ingresso foi confirmado.

🎬 Filme: {movie_title}
📅 Sessão: {session_datetime}
💺 Assento: {seat_row}{seat_column}
🎫 Código do Ingresso: {ticket_code}

Obrigado por usar o CineReserve - Cinépolis Natal!
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_FROM,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f"Email sent to {user_email}"
