from __future__ import annotations

from fastapi.testclient import TestClient


def test_ordo_json_by_default(client: TestClient):
    response = client.get("/en/api/v5/ordo")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")


def test_ordo_pdf_when_requested(client: TestClient):
    response = client.get("/en/api/v5/ordo?format=pdf&variant=a4")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_invalid_pdf_variant_returns_422(client: TestClient):
    response = client.get("/en/api/v5/ordo?format=pdf&variant=unknown-size")

    assert response.status_code == 422
    detail = response.json().get("detail", [])
    assert "value is not a valid enumeration member" in str(detail)
