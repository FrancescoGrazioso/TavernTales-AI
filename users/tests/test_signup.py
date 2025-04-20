import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_signup(client):
    url = reverse("signup")
    data = {"username": "frodo", "email": "frodo@shire.me", "password": "Ring12345"}
    resp = client.post(url, data)
    assert resp.status_code == 201
    assert resp.data["username"] == "frodo"
