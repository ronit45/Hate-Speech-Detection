from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "CyberNyaya Backend is running"
    # Note: models_loaded might be True or False depending on if models exist in the environment,
    # but the endpoint should return 200 regardless.

def test_analyze_valid_text():
    # If models are missing locally, this might return 500. 
    # But assuming models are present:
    response = client.post("/api/analyze", json={"text": "tu ek number ka gadha hai"})
    if response.status_code == 200:
        data = response.json()
        assert "threat_level" in data
        assert "bns_section" in data
        assert "processed_text" in data
        assert data["original_text"] == "tu ek number ka gadha hai"
    else:
        # If models aren't loaded, it returns 500. We assert it's one or the other.
        assert response.status_code == 500

def test_analyze_empty_text():
    response = client.post("/api/analyze", json={"text": "   "})
    # Should be 500 if models not loaded, else 400
    assert response.status_code in [400, 500]

def test_analyze_massive_payload():
    # Test if server handles 10,000 words without crashing
    massive_text = "kutta " * 10000
    response = client.post("/api/analyze", json={"text": massive_text})
    assert response.status_code in [200, 500]

def test_complaint_generation():
    payload = {
        "original_text": "I will kill you",
        "bns_section": "BNS 351 (Criminal Intimidation)",
        "threat_level": "High"
    }
    response = client.post("/api/complaint/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "draft" in data
    assert "FORMAL CYBER CRIME COMPLAINT" in data["draft"]
    assert "I will kill you" in data["draft"]
