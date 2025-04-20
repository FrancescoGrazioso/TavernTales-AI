import pytest
from rest_framework.test import APIClient
from users.models import User
from game.models import Party

@pytest.fixture
def api_client(db):
    """
    Restituisce un APIClient autenticato con JWT per i test delle API Party/Session.
    """
    username = "legolas"
    password = "Arrow123"
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()

    # Ottieni un token JWT dall'endpoint di login
    from django.urls import reverse
    token_url = reverse("login")  # TokenObtainPairView registrato come "login"
    resp = client.post(token_url, {"username": username, "password": password}, format="json")
    assert resp.status_code == 200, resp.data
    token = resp.data["access"]

    # Imposta l'header Authorization per tutte le richieste successive
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user

@pytest.mark.django_db
def test_create_party(api_client):
    client, user = api_client
    resp = client.post("/api/parties/", {"name": "Compagnia dell'Anello"}, format="json")
    assert resp.status_code == 201
    assert Party.objects.filter(owner=user).exists()