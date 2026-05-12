"""
Pytest configuration and fixtures for API tests.

Provides:
- TestClient for FastAPI app
- Fresh activities database for each test (isolation)
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Provide a fresh copy of activities for each test to ensure test isolation.
    
    Automatically resets the global activities dict to a clean state before each test,
    preventing test pollution and side effects.
    """
    # Create a deep copy of the original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and intramural games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis training and court time for all skill levels",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["ryan@mergington.edu", "maya@mergington.edu"]
        },
        "Visual Arts": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Join our orchestra and perform at school events",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking skills",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jason@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through experiments",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["noah@mergington.edu", "grace@mergington.edu"]
        }
    }
    
    # Deep copy and inject into the app module
    fresh_copy = copy.deepcopy(original_activities)
    monkeypatch.setattr("src.app.activities", fresh_copy)
    
    return fresh_copy
