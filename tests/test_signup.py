"""
Tests for the POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_signup_new_student_success(client, fresh_activities):
    """Test successful signup of a new student for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participant_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_participant_count + 1


def test_signup_duplicate_student_fails(client, fresh_activities):
    """Test that a student cannot signup twice for the same activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    initial_participant_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert len(fresh_activities[activity_name]["participants"]) == initial_participant_count


def test_signup_invalid_activity_not_found(client, fresh_activities):
    """Test that signup fails for a non-existent activity."""
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_multiple_students_same_activity(client, fresh_activities):
    """Test that multiple different students can signup for the same activity."""
    # Arrange
    activity_name = "Programming Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in fresh_activities[activity_name]["participants"]
    assert email2 in fresh_activities[activity_name]["participants"]


def test_signup_same_student_different_activities(client, fresh_activities):
    """Test that the same student can signup for multiple different activities."""
    # Arrange
    email = "student@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email in fresh_activities[activity1]["participants"]
    assert email in fresh_activities[activity2]["participants"]
