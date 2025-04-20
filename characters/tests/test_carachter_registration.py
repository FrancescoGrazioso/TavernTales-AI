import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from characters.models import Character


@pytest.fixture
def auth_client(db):
    """
    Restituisce un APIClient già autenticato via JWT.
    """
    username = "aragorn"
    password = "Anduril123"
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()

    # ottieni token JWT
    token_url = reverse("login")  # alias di TokenObtainPairView
    resp = client.post(
        token_url, {"username": username, "password": password}, format="json"
    )
    assert resp.status_code == 200, resp.data
    token = resp.data["access"]

    # imposta header Authorization
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


@pytest.mark.django_db
def test_create_character(auth_client):
    client, user = auth_client
    url = reverse("character-list")
    payload = {
        "name": "Aragorn",
        "char_class": "ranger",
        "race": "Human",
        "level": 5,
        "strength": 16,
        "dexterity": 13,
        "constitution": 14,
        "intelligence": 10,
        "wisdom": 12,
        "charisma": 14,
        "hp_max": 58,
        "hp_current": 58,
    }
    resp = client.post(url, payload, format="json")
    assert resp.status_code == 201
    assert Character.objects.filter(user=user, name="Aragorn").exists()
