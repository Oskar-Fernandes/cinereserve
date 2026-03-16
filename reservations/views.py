import uuid
from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from .tasks import release_seat_lock, send_ticket_confirmation_email
from movies.models import Session, Seat
from django.conf import settings


class ReserveSeatView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, session_id, seat_id):
        try:
            session = Session.objects.get(id=session_id)
            seat = Seat.objects.get(id=seat_id)
        except (Session.DoesNotExist, Seat.DoesNotExist):
            return Response({'error': 'Sessao ou assento nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if seat.room != session.room:
            return Response({'error': 'Assento nao pertence a sala desta sessao.'}, status=status.HTTP_400_BAD_REQUEST)

        lock_key = f"seat_lock:{session_id}:{seat_id}"
        if cache.get(lock_key):
            return Response({'error': 'Assento temporariamente reservado.'}, status=status.HTTP_409_CONFLICT)

        if Ticket.objects.filter(session=session, seat=seat, status='purchased').exists():
            return Response({'error': 'Assento ja comprado.'}, status=status.HTTP_409_CONFLICT)

        timeout = getattr(settings, 'SEAT_LOCK_TIMEOUT', 600)
        cache.set(lock_key, request.user.id, timeout=timeout)

        release_seat_lock.apply_async(
            args=[session_id, seat_id],
            countdown=timeout
        )

        return Response({
            'message': 'Assento reservado por 10 minutos. Finalize o pagamento.',
            'session_id': session_id,
            'seat_id': seat_id,
            'lock_expires_in': timeout,
        }, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, session_id, seat_id):
        lock_key = f"seat_lock:{session_id}:{seat_id}"
        lock = cache.get(lock_key)

        if not lock:
            return Response({'error': 'Nenhuma reserva ativa encontrada. Reserve o assento primeiro.'}, status=status.HTTP_400_BAD_REQUEST)

        if lock != request.user.id:
            return Response({'error': 'Esta reserva pertence a outro usuario.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            session = Session.objects.get(id=session_id)
            seat = Seat.objects.get(id=seat_id)
        except (Session.DoesNotExist, Seat.DoesNotExist):
            return Response({'error': 'Sessao ou assento nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if Ticket.objects.filter(session=session, seat=seat, status='purchased').exists():
            return Response({'error': 'Assento ja comprado.'}, status=status.HTTP_409_CONFLICT)

        ticket = Ticket.objects.create(
            user=request.user,
            session=session,
            seat=seat,
            status=Ticket.Status.PURCHASED,
            ticket_code=str(uuid.uuid4()).upper()[:12],
        )

        cache.delete(lock_key)

        send_ticket_confirmation_email.delay(
            user_email=request.user.email,
            ticket_code=ticket.ticket_code,
            movie_title=session.movie.title,
            session_datetime=str(session.datetime),
            seat_row=seat.row,
            seat_column=seat.column,
        )

        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Ticket.objects.filter(
            user=self.request.user
        ).select_related('session', 'seat').order_by('-created_at')
