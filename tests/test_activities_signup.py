def test_signup_for_activity_succeeds_and_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
    payload = response.json()
    refreshed = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {student_email} for {activity_name}"
    assert student_email in refreshed[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{unknown_activity}/signup", params={"email": student_email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_for_activity_requires_email_query_param(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
