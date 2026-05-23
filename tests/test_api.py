from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import configure_database
from app.main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    configure_database(str(tmp_path / "api-test.db"))

    with TestClient(app) as test_client:
        yield test_client


def test_task_api_flow(client: TestClient) -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "API task",
            "description": "Created through HTTP",
            "priority": "high",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["priority"] == "high"
    assert created["done"] is False

    complete_response = client.patch(f"/tasks/{created['id']}/complete")

    assert complete_response.status_code == 200
    assert complete_response.json()["done"] is True

    open_response = client.get("/tasks/open")

    assert open_response.status_code == 200
    assert open_response.json() == []


def test_complete_unknown_task_returns_404(client: TestClient) -> None:
    response = client.patch("/tasks/999/complete")

    assert response.status_code == 404


def test_invalid_task_priority_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Invalid priority", "priority": "urgent"},
    )

    assert response.status_code == 422
