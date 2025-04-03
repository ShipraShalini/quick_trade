def test_health(client):
    """Test to check if app starts."""
    # Act
    response = client.get("/healthcheck")

    # Assert
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "healthy"
    assert response.json()["success"] is True
