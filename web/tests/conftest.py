"""
This file contains the configurations and some baseline test fixtures for testing using pytest.
"""

import pytest
from fastapi.testclient import TestClient
from app import app as fastapi_app


@pytest.fixture(scope="session")
def test_client():
    # Fixture for creating the test client
    testing_client = TestClient(fastapi_app)
    yield testing_client


@pytest.fixture(scope="function")
def create_part():
    # Fixture for creating a part
    testing_client = TestClient(fastapi_app)
    response = testing_client.post("/part", json={"part_name": "test_part"})
    return response


@pytest.fixture(scope="function")
def create_assembly(create_part):
    # Fixture for creating an assembly
    testing_client = TestClient(fastapi_app)
    response = testing_client.post(
        "/assembly",
        json={"assembly_name": "test_assembly", "part_names": ["test_part"]},
    )
    return response


@pytest.fixture(scope="function")
def create_multi_level_assembly(create_assembly):
    # Fixture for creating a multi-level assembly
    testing_client = TestClient(fastapi_app)
    testing_client.post("/part", json={"part_name": "test_part2"})
    response = testing_client.post(
        "/assembly",
        json={
            "assembly_name": "test_assembly2",
            "part_names": ["test_part2"],
            "subassembly_names": ["test_assembly"],
        },
    )
    return response
