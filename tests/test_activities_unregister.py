def test_unregister_participant_succeeds_and_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": existing_email}
    )
    payload = response.json()
    refreshed = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in refreshed[activity_name]["participants"]


def test_unregister_participant_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants", params={"email": existing_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_participant_rejects_unknown_participant(client):
    # Arrange
    activity_name = "Chess Club"
    unknown_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": unknown_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_unregister_participant_requires_email_query_param(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants")

    # Assert
    assert response.status_code == 422
