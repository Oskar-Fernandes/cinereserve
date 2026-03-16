import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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


@pytest.mark.django_db
def test_register(client):
    response = client.post('/api/users/register/', {
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201


@pytest.mark.django_db
def test_login(client, user):
    response = client.post('/api/users/login/', {
        'email': 'test@test.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access' in response.data


@pytest.mark.django_db
def test_profile(client, user):
    client.force_authenticate(user=user)
    response = client.get('/api/users/profile/')
    assert response.status_code == 200
    assert response.data['email'] == user.email