# Tests for input validation
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_invalid_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "organization": "ABC Technologies",
            "recipients": [
                {
                    "name": "Rishi Raj",
                    "email": "invalid-email",
                    "course": "Python Development"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_empty_recipients():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "organization": "ABC Technologies",
            "recipients": []
        }
    )

    assert response.status_code == 422