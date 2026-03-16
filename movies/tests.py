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
def movie(db):
    return Movie.objects.create(
        title='Test Movie',
        description='A test movie',
        duration_minutes=120,
        genre='Action'
    )


@pytest.fixture
def room(db):
    return Room.objects.create(name='Room 1', rows=5, columns=5)


@pytest.fixture
def session(db, movie, room):
    return Session.objects.create(
        movie=movie,
        room=room,
        datetime=timezone.now()
    )


@pytest.fixture
def seats(db, room):
    seats = []
    for row in ['A', 'B']:
        for col in range(1, 4):
            seats.append(Seat.objects.create(room=room, row=row, column=col))
    return seats


@pytest.mark.django_db
def test_list_movies(client, movie):
    response = client.get('/api/movies/')
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_list_sessions(client, session):
    response = client.get(f'/api/movies/{session.movie.id}/sessions/')
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_seat_map(client, user, session, seats):
    client.force_authenticate(user=user)
    response = client.get(f'/api/movies/sessions/{session.id}/seats/')
    assert response.status_code == 200
    assert response.data['count'] == len(seats)