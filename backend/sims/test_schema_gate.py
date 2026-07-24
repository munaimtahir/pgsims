from django.urls import reverse
from rest_framework.test import APIClient
import yaml


def test_openapi_schema_endpoint_exposes_active_contract(db):
    client = APIClient()

    response = client.get(reverse("schema"))

    assert response.status_code == 200
    payload = yaml.safe_load(response.content)
    assert payload["info"]["title"] == "PGSIMS API"
    assert "openapi" in payload
    assert "/api/auth/login/" in payload["paths"]
    assert "/api/academics/residents/me/summary/" in payload["paths"]
