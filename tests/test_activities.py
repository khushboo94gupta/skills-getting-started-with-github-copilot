"""
Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """Test that GET /activities returns all available activities."""
    # Arrange
    expected_activity_count = len(fresh_activities)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_returns_correct_structure(client, fresh_activities):
    """Test that each activity has the correct data structure."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert all(field in activity_data for field in required_fields)
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_participants_populated(client, fresh_activities):
    """Test that participants are correctly returned for each activity."""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert activities["Chess Club"]["participants"] == expected_chess_participants
