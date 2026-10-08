# Tests for certificate retrieval
import sqlite3

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_certificate_retrieval():
    db = sqlite3.connect("certificates.db")
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id
        FROM certificates
        WHERE status = 'completed'
        ORDER BY id DESC
        LIMIT 1
        """
    )

    result = cursor.fetchone()
    db.close()

    assert result is not None

    certificate_id = result[0]

    response = client.get(
        f"/api/certificates/{certificate_id}"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0