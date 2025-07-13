"""
Test suite for MCP server functionality using pytest.
Tests Garmin connection and resource methods independently.
"""

import os
import pytest
import time
from datetime import datetime

# Add src to path so we can import modules
import sys
sys.path.insert(0, 'src')

from garmin.client import Garmin


@pytest.fixture(scope="session")
def garmin_client():
    """Create a Garmin client for testing."""
    # Try to read existing token first
    tokens = None
    try:
        with open("tokenstore", "r") as f:
            tokens = f.read().strip()
        print("Found existing tokenstore")
    except FileNotFoundError:
        print("No existing tokenstore found")
    
    # Only get credentials if no tokenstore exists
    email = None
    password = None
    if not tokens:
        email = os.getenv("GARMIN_EMAIL")
        password = os.getenv("GARMIN_PASSWORD")
        
        if not email or not password:
            pytest.skip("GARMIN_EMAIL and GARMIN_PASSWORD environment variables must be set")
        
        print(f"Email: {email}")
    else:
        print("Using existing tokenstore, credentials not needed")
    
    # Test login
    start_time = time.time()
    print("Attempting login...")
    client = Garmin(email or "", password or "", tokens=tokens)
    tokens = client.login()
    login_time = time.time() - start_time
    print(f"Login successful in {login_time:.2f} seconds")
    
    # Save token
    with open("tokenstore", "w") as f:
        f.write(tokens)
    print("Token saved to tokenstore")
    
    return client


def test_garmin_connection(garmin_client):
    """Test that Garmin client is properly connected."""
    assert garmin_client is not None
    assert hasattr(garmin_client, 'get_user_profile')
    assert hasattr(garmin_client, 'get_activities')
    assert hasattr(garmin_client, 'get_comprehensive_fitness_data')


def test_get_user_profile(garmin_client):
    """Test the get_user_profile method."""
    start_time = time.time()
    print("Calling get_user_profile...")
    
    profile = garmin_client.get_user_profile()
    profile_time = time.time() - start_time
    print(f"get_user_profile completed in {profile_time:.2f} seconds")
    
    assert profile is not None
    print(f"Profile type: {type(profile)}")
    
    if hasattr(profile, '__dict__'):
        print(f"Profile attributes: {list(profile.__dict__.keys())}")
    
    # Test str conversion
    start_time = time.time()
    print("Converting to string...")
    result = str(profile)
    str_time = time.time() - start_time
    print(f"str conversion completed in {str_time:.2f} seconds")
    
    assert isinstance(result, str)
    assert len(result) > 0
    print(f"Result length: {len(result)} characters")
    
    # Check for timeout (should complete in reasonable time)
    assert profile_time < 15, f"get_user_profile took too long: {profile_time:.2f} seconds"
    assert str_time < 5, f"str conversion took too long: {str_time:.2f} seconds"


def test_get_activities(garmin_client):
    """Test the get_activities method."""
    start_time = time.time()
    print("Calling get_activities...")
    
    activities = garmin_client.get_activities(start=0, limit=5, activitytype="running")
    activities_time = time.time() - start_time
    print(f"get_activities completed in {activities_time:.2f} seconds")
    
    assert activities is not None
    assert isinstance(activities, list)
    print(f"Number of activities: {len(activities)}")
    
    if len(activities) > 0:
        assert isinstance(activities[0], dict)
        print(f"First activity keys: {list(activities[0].keys())}")
    
    # Check for timeout
    assert activities_time < 15, f"get_activities took too long: {activities_time:.2f} seconds"


def test_comprehensive_fitness_data(garmin_client):
    """Test the get_comprehensive_fitness_data method."""
    start_time = time.time()
    print("Calling get_comprehensive_fitness_data...")
    
    fitness_data = garmin_client.get_comprehensive_fitness_data(limit_activities=5)
    fitness_time = time.time() - start_time
    print(f"get_comprehensive_fitness_data completed in {fitness_time:.2f} seconds")
    
    assert fitness_data is not None
    print(f"Fitness data type: {type(fitness_data)}")
    
    # Test str conversion
    result = str(fitness_data)
    assert isinstance(result, str)
    assert len(result) > 0
    print(f"str result length: {len(result)} characters")
    
    # Check for timeout
    assert fitness_time < 15, f"get_comprehensive_fitness_data took too long: {fitness_time:.2f} seconds"


def test_mcp_resource_simulation(garmin_client):
    """Simulate the MCP resource calls to identify timeout issues."""
    print("\n=== Simulating MCP Resource Calls ===")
    
    # Simulate get_user_profile resource
    start_time = time.time()
    try:
        garmin_instance = Garmin.get_instance()
        profile = garmin_instance.get_user_profile()
        result = str(profile)
        duration = time.time() - start_time
        print(f"✅ get_user_profile resource simulation: {duration:.2f}s")
        assert duration < 15, "Resource would timeout in MCP"
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ get_user_profile resource simulation failed after {duration:.2f}s: {e}")
        raise
    
    # Simulate get_activities resource
    start_time = time.time()
    try:
        activities = Garmin.get_instance().get_activities(start=0, limit=10, activitytype="running")
        result = str(activities)
        duration = time.time() - start_time
        print(f"✅ get_activities resource simulation: {duration:.2f}s")
        assert duration < 15, "Resource would timeout in MCP"
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ get_activities resource simulation failed after {duration:.2f}s: {e}")
        raise
    
    # Simulate get_user_fitness_data resource
    start_time = time.time()
    try:
        fitness_data = Garmin.get_instance().get_comprehensive_fitness_data(limit_activities=15)
        result = str(fitness_data)
        duration = time.time() - start_time
        print(f"✅ get_user_fitness_data resource simulation: {duration:.2f}s")
        assert duration < 15, "Resource would timeout in MCP"
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ get_user_fitness_data resource simulation failed after {duration:.2f}s: {e}")
        raise