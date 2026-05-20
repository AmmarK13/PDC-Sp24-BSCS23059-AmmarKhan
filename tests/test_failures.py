from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_route_has_student_header():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["X-Student-ID"] == "BSCS23059"


def test_chat_route_returns_response():
    response = client.post(
        "/chat",
        json={"prompt": "Explain distributed systems"}
    )

    assert response.status_code == 200
    assert "response" in response.json()
    assert response.headers["X-Student-ID"] == "BSCS23059"


def test_circuit_breaker_handles_llm_failure():
    responses = []

    for _ in range(6):
        response = client.post(
            "/chat",
            json={"prompt": "Test failure handling"}
        )
        responses.append(response.json()["response"])

    assert any("Fallback response" in r for r in responses)