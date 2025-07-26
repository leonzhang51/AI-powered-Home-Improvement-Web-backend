"""
Test project endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def get_auth_headers(client: TestClient) -> dict:
    """Helper to get authentication headers."""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "test@example.com", "password": "testpassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_project(client: TestClient):
    """Test project creation."""
    headers = get_auth_headers(client)
    
    project_data = {
        "title": "Living Room Renovation",
        "description": "Modernize my living room with contemporary style",
        "room_type": "living_room",
        "style_preference": "modern",
        "budget_range": "1000-5000"
    }
    
    response = client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers,
        params={"auto_process": False}  # Skip AI processing for test
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    project = data["project"]
    assert project["title"] == "Living Room Renovation"
    assert project["room_type"] == "living_room"


def test_get_projects(client: TestClient):
    """Test getting user projects."""
    headers = get_auth_headers(client)
    
    # Create a project first
    project_data = {
        "title": "Kitchen Renovation",
        "description": "Update kitchen with modern appliances",
        "room_type": "kitchen",
        "style_preference": "contemporary",
        "budget_range": "5000-10000"
    }
    
    client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers,
        params={"auto_process": False}
    )
    
    # Get projects
    response = client.get("/api/v1/projects/", headers=headers)
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["title"] == "Kitchen Renovation"


def test_get_project_by_id(client: TestClient):
    """Test getting a specific project."""
    headers = get_auth_headers(client)
    
    # Create a project
    project_data = {
        "title": "Bathroom Renovation",
        "description": "Modern bathroom design",
        "room_type": "bathroom",
        "style_preference": "minimalist",
        "budget_range": "2000-5000"
    }
    
    create_response = client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers,
        params={"auto_process": False}
    )
    
    project_id = create_response.json()["project"]["id"]
    
    # Get the project
    response = client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert response.status_code == 200
    project = response.json()
    assert project["title"] == "Bathroom Renovation"


def test_unauthorized_access(client: TestClient):
    """Test unauthorized access to projects."""
    response = client.get("/api/v1/projects/")
    assert response.status_code == 401
