def test_get_activities_returns_expected_shape(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload

    for activity in payload.values():
        assert required_fields.issubset(activity.keys())
        assert isinstance(activity["participants"], list)


def test_get_activities_returns_no_cache_headers(client):
    # Arrange
    expected_cache_control = "no-store, no-cache, must-revalidate, max-age=0"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers.get("cache-control") == expected_cache_control
    assert response.headers.get("pragma") == "no-cache"
    assert response.headers.get("expires") == "0"
