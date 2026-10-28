def payload(): return {"incident_type":"timeout","error_message":"Vertex request failed","service_name":"api","context":"intermittent"}
def test_mocked_analysis(client):
    response = client.post("/api/v1/analyze", json=payload()); assert response.status_code == 200; assert response.json()["severity"] == "high"
def test_invalid_incident(client):
    response = client.post("/api/v1/analyze", json={}); assert response.status_code == 422
def test_request_id_propagates(client):
    response = client.get("/health/live", headers={"X-Request-ID":"trace-me"}); assert response.headers["x-request-id"] == "trace-me"
