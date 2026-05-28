def test_activity_name_matching_is_case_sensitive(client):
    # Arrange
    activity_name_with_wrong_case = "chess club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name_with_wrong_case}/signup", params={"email": student_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_and_unregister_round_trip_restores_state(client):
    # Arrange
    activity_name = "Science Club"
    student_email = "round.trip@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": student_email}
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": student_email}
    )
    refreshed = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert student_email not in refreshed[activity_name]["participants"]
