from django.urls import path
from .views import ReserveSeaView, CheckoutView, MyTicketsView

urlpatterns = [
    path('sessions/<int:session_id>/seats/<int:seat_id>/reserve/', ReserveSeaView.as_view(), name='reserve_seat'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-tickets/', MyTicketsView.as_view(), name='my_tickets'),
]