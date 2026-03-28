from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Integration Layer Running" in resp.json().get("status", "")


def test_ivr_start_returns_session_and_menu():
    resp = client.post("/ivr/start", json={"caller": "pytest"})
    assert resp.status_code == 200

    body = resp.json()
    assert isinstance(body.get("session_id"), str)
    assert len(body["session_id"]) > 0
    assert "Welcome to City Hospital IVR" in body.get("message", "")


def test_ivr_input_returns_valid_menu_response():
    start_resp = client.post("/ivr/start", json={"caller": "pytest"})
    session_id = start_resp.json()["session_id"]

    resp = client.post("/ivr/input", json={"session_id": session_id, "digit": "4"})
    assert resp.status_code == 200
    assert "Cardiology" in resp.json().get("message", "")


def test_ai_message_maps_intent_to_ivr_option():
    resp = client.post(
        "/ai/message",
        json={"message": "doctor availability", "session_id": "seed-session"},
    )
    assert resp.status_code == 200

    body = resp.json()
    assert body["intent"] == "doctor"
    assert body["menu"] == "doctor"
    assert body["ivr_option"] == "2"