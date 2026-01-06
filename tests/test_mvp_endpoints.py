from fastapi.testclient import TestClient

from azure_api_mock.app import create_app


def test_healthz():
    client = TestClient(create_app())
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_projects_demo():
    client = TestClient(create_app())
    r = client.get("/demo-org/_apis/projects", params={"api-version": "7.0"})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    assert any(p["name"] == "demo-project" for p in body["value"])


def test_list_repos_demo():
    client = TestClient(create_app())
    r = client.get(
        "/demo-org/demo-project/_apis/git/repositories",
        params={"api-version": "7.0"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    assert any(repo["name"] == "demo-repo" for repo in body["value"])
