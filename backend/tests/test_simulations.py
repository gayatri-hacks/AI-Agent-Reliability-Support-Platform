def test_simulations_are_protected(client): assert client.get("/api/v1/simulations").status_code == 404
def test_simulated_timeout(client): assert client.post("/api/v1/simulations/timeout", headers={"X-Simulation-Token":"test-token"}).status_code == 504
