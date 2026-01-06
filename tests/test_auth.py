import base64

from fastapi.testclient import TestClient

from azure_api_mock.app import create_app


def _basic_header(token: str) -> str:
    b = base64.b64encode(f":{token}".encode("utf-8")).decode("ascii")
    return f"Basic {b}"


def test_auth_none_allows_requests(monkeypatch):
    monkeypatch.setenv("ADO_MOCK_AUTH_MODE", "none")
    client = TestClient(create_app())
    r = client.get("/demo-org/_apis/projects", params={"api-version": "7.0"})
    assert r.status_code == 200


def test_auth_pat_requires_header(monkeypatch):
    monkeypatch.setenv("ADO_MOCK_AUTH_MODE", "pat")
    monkeypatch.setenv("ADO_MOCK_TOKEN", "t1")

    client = TestClient(create_app())
    r = client.get("/demo-org/_apis/projects", params={"api-version": "7.0"})
    assert r.status_code == 401


def test_auth_pat_rejects_wrong_token(monkeypatch):
    monkeypatch.setenv("ADO_MOCK_AUTH_MODE", "pat")
    monkeypatch.setenv("ADO_MOCK_TOKEN", "t1")

    client = TestClient(create_app())
    r = client.get(
        "/demo-org/_apis/projects",
        params={"api-version": "7.0"},
        headers={"Authorization": _basic_header("wrong")},
    )
    assert r.status_code == 403


def test_auth_pat_accepts_token(monkeypatch):
    monkeypatch.setenv("ADO_MOCK_AUTH_MODE", "pat")
    monkeypatch.setenv("ADO_MOCK_TOKEN", "t1")

    client = TestClient(create_app())
    r = client.get(
        "/demo-org/_apis/projects",
        params={"api-version": "7.0"},
        headers={"Authorization": _basic_header("t1")},
    )
    assert r.status_code == 200
