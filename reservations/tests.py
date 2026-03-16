import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from movies.models import Movie, Room, Session, Seat
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='password123'
    )


@pytest.fixture
def session_with_seat(db):
    movie = Movie.objects.create(
        title='Test Movie',
        description='desc',
        duration_minutes=100,
        genre='Drama'
    )
    room = Room.objects.create(name='Room 1', rows=3, columns=3)
    seat = Seat.objects.create(room=room, row='A', column=1)
    session = Session.objects.create(
        movie=movie,
        room=room,
        datetime=timezone.now()
    )
    return session, seat


@pytest.mark.django_db
def test_reserve_seat(client, user, session_with_seat):
    session, seat = session_with_seat
    client.force_authenticate(user=user)
    response = client.post(
        f'/api/reservations/sessions/{session.id}/seats/{seat.id}/reserve/'
    )
    assert response.status_code == 200
    assert 'lock_expires_in' in response.data


@pytest.mark.django_db
def test_checkout(client, user, session_with_seat):
    session, seat = session_with_seat
    client.force_authenticate(user=user)
    client.post(f'/api/reservations/sessions/{session.id}/seats/{seat.id}/reserve/')
    response = client.post(
        f'/api/reservations/sessions/{session.id}/seats/{seat.id}/checkout/'
    )
    assert response.status_code == 201
    assert 'ticket_code' in response.data


@pytest.mark.django_db
def test_my_tickets(client, user, session_with_seat):
    session, seat = session_with_seat
    client.force_authenticate(user=user)
    client.post(f'/api/reservations/sessions/{session.id}/seats/{seat.id}/reserve/')
    client.post(f'/api/reservations/sessions/{session.id}/seats/{seat.id}/checkout/')
    response = client.get('/api/reservations/my-tickets/')
    assert response.status_code == 200
    assert response.data['count'] == 1