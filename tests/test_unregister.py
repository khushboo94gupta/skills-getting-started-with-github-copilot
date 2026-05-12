"""
Tests for the DELETE /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_unregister_existing_participant_success(client, fresh_activities):
    """Test successful unregistration of an existing participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    initial_participant_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_participant_count - 1


def test_unregister_non_existent_participant_fails(client, fresh_activities):
    """Test that unregistering a non-existent participant fails with 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    initial_participant_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert len(fresh_activities[activity_name]["participants"]) == initial_participant_count


def test_unregister_from_invalid_activity_fails(client, fresh_activities):
    """Test that unregistering from a non-existent activity fails with 404."""
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_all_participants_from_activity(client, fresh_activities):
    """Test that all participants can be unregistered from an activity."""
    # Arrange
    activity_name = "Chess Club"
    participants_copy = fresh_activities[activity_name]["participants"].copy()
    
    # Act & Assert
    for email in participants_copy:
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email not in fresh_activities[activity_name]["participants"]
    
    # Final Assert: Activity should have no participants
    assert len(fresh_activities[activity_name]["participants"]) == 0


def test_unregister_then_signup_again(client, fresh_activities):
    """Test that a student can unregister and then sign up again."""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up
    
    # Act - Unregister
    response1 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Unregistered
    assert response1.status_code == 200
    assert email not in fresh_activities[activity_name]["participants"]
    
    # Act - Sign up again
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Signed up again
    assert response2.status_code == 200
    assert email in fresh_activities[activity_name]["participants"]


def test_unregister_double_attempt_fails(client, fresh_activities):
    """Test that attempting to unregister the same participant twice fails on the second attempt."""
    # Arrange
    activity_name = "Tennis Club"
    email = "ryan@mergington.edu"  # Already signed up
    
    # Act - First unregister
    response1 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - First unregister successful
    assert response1.status_code == 200
    assert email not in fresh_activities[activity_name]["participants"]
    
    # Act - Second unregister (should fail)
    response2 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Second unregister fails with 400
    assert response2.status_code == 400
    assert response2.json() == {"detail": "Student is not signed up for this activity"}
