"""
This file contains tests for the methods in the app.py file
"""

import json


def test_hello_world(test_client):
    """
    GIVEN a FastAPI application
    WHEN the '/' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": "Hello, World"}


def test_health(test_client):
    """
    GIVEN a FastAPI application
    WHEN the '/health' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Running"}


def test_post_part(test_client):
    """
    GIVEN a FastAPI application
    WHEN the '/part' endpoint is requested (POST)
    THEN check that the response code is valid, the expected response is returned,
    and data is successfully posted
    """

    # Providing invalid data
    response = test_client.post("/part", json={"part": "test_part"})
    assert response.status_code == 422

    # Providing no data
    response = test_client.post("/part")
    assert response.status_code == 422

    # Providing valid data
    response = test_client.post("/part", json={"part_name": "test_part"})
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["status"] == "Success"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_part(test_client, create_part):
    """
    GIVEN a FastAPI application
    WHEN the '/part' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """
    # Getting all created parts
    response = test_client.get("/part")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    data_json = json.loads(response_json["data"])
    assert len(data_json) != 0
    assert json.loads(data_json[0])["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_part_by_name(test_client, create_part):
    """
    GIVEN a FastAPI application
    WHEN the '/part/{part_name}' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting part by name
    response = test_client.get("/part/test_part")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert json.loads(response_json["data"])["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_delete_part(test_client, create_part):
    """
    GIVEN a FastAPI application
    WHEN the '/part/{part_name}' endpoint is requested (DELETE)
    THEN check that the response code is valid, the expected response is returned,
    and the data is successfully deleted
    """

    response = test_client.delete("/part/test123")
    assert response.status_code == 403

    response = test_client.delete("/part/test_part")
    assert response.status_code == 200

    response = test_client.get("/part/test_part")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] is None

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_post_assembly(test_client, create_part):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly' endpoint is requested (POST)
    THEN check that the response code is valid, the expected response is returned,
    and the data is successfully posted
    """

    # Providing part name that doesn't exist
    response = test_client.post(
        "/assembly",
        json={"assembly_name": "test_assembly", "part_names": ["test_part2"]},
    )
    assert response.status_code == 404

    # Not providing assembly name
    response = test_client.post("/assembly", json={"part_names": ["test_part2"]})
    assert response.status_code == 422

    # Providing valid data
    response = test_client.post(
        "/assembly",
        json={"assembly_name": "test_assembly", "part_names": ["test_part"]},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert data_json["id"] == "test_assembly"
    assert data_json["children"][0]["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_assembly(test_client, create_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting all created assemblies
    response = test_client.get("/assembly")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert json.loads(data_json[0])["id"] == "test_assembly"
    assert json.loads(data_json[0])["children"][0]["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_assembly_by_name(test_client, create_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting invalid assembly
    response = test_client.get("/assembly/test_assembly123")
    assert response.status_code == 403

    # Getting valid assembly
    response = test_client.get("/assembly/test_assembly")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    assert json.loads(response_json["data"])["id"] == "test_assembly"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_detach_part_assembly(test_client, create_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}' endpoint is requested (PUT)
    THEN check that the response code is valid, the expected response is returned,
    and the data is successfully updated
    """

    # Providing non existing part
    response = test_client.put(
        "/assembly/test_assembly/child/test_part2",
    )
    assert response.status_code == 403

    # Providing non-existing assembly
    response = test_client.put(
        "/assembly/test_assembly1234/child/test_part",
    )
    assert response.status_code == 403

    # Providing existing part and assembly
    response = test_client.put(
        "/assembly/test_assembly/child/test_part",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    data_json = json.loads(response_json["data"])
    assert data_json["id"] == "test_assembly"
    assert "children" not in data_json

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_attach_part_assembly(test_client, create_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}' endpoint is requested (POST)
    THEN check that the response code is valid, the expected response is returned,
    and the data is successfully updated
    """

    # Providing part that doesn't exist
    response = test_client.post(
        "/assembly/test_assembly/child/test_part2",
    )
    assert response.status_code == 403

    # Providing assembly that doesn't exist
    response = test_client.post(
        "/assembly/test_assembly1234/child/test_part",
    )
    assert response.status_code == 403

    # Creating new part to attach
    response = test_client.post("/part", json={"part_name": "test_part2"})
    assert response.status_code == 201

    # Attaching existing assembly and part
    response = test_client.post(
        "/assembly/test_assembly/child/test_part2",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"

    data_json = json.loads(response_json["data"])
    assert "children" in data_json
    assert data_json["children"][1]["id"] == "test_part2"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_top_assembly(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/top_assembly' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting top assemblies
    response = test_client.get("/top_assembly")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert json.loads(data_json[0])["id"] == "test_assembly2"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_subassembly(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/subassembly' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting subassemblies
    response = test_client.get("/subassembly")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    data_json = json.loads(response_json["data"])
    assert len(data_json) != 0
    assert json.loads(data_json[0])["id"] == "test_assembly"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_component_part(test_client, create_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/component' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting component part
    response = test_client.get("/component")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert json.loads(data_json[0])["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_orphan(test_client, create_part):
    """
    GIVEN a FastAPI application
    WHEN the '/orphan' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Checking orphan part
    response = test_client.get("/orphan")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert json.loads(data_json[0])["id"] == "test_part"

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_assembly_first_children(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}/first' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting top-level assembly's first-level children
    response = test_client.get("/assembly/test_assembly2/first")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])

    # Checking if all first-level children are valid
    first_level_children = {"test_part2", "test_assembly"}
    result_first_level_children = set()
    for item in data_json:
        result_first_level_children.add(json.loads(item)["id"])

    assert result_first_level_children == first_level_children

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_assembly_children(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}/first' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting all top-level assembly's children
    response = test_client.get("/assembly/test_assembly2/children")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])

    # Checking if all children are valid
    children = {"test_part2", "test_assembly", "test_part"}
    result_children = set()
    for item in data_json:
        result_children.add(json.loads(item)["id"])

    assert result_children == children

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_assembly_leaves(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/assembly/{assembly_name}/leaves' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting leaves of top-level assembly
    response = test_client.get("/assembly/test_assembly2/leaves")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])

    # Checking if all leaves are valid
    leaves = {"test_part", "test_part2"}
    result_leaves = set()
    for item in data_json:
        result_leaves.add(json.loads(item)["id"])

    assert result_leaves == leaves

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_part_ancestors(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/part/{part_name}/parents' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Getting all ancestors of a leaf part
    response = test_client.get("/part/test_part/parents")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["data"]) != 0
    data_json = json.loads(response_json["data"])
    assert len(data_json) != 0

    # Checking if all ancestors are valid
    ancestors = {"test_assembly", "test_assembly2"}
    result_ancestors = set()
    for item in data_json:
        result_ancestors.add(json.loads(item)["id"])

    assert result_ancestors == ancestors

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_post_project(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/project/{project_name}' endpoint is requested (POST)
    THEN check that the response code is valid, the expected response is returned,
    and the data is successfully posted
    """

    # Saving assembly project
    response = test_client.post("/project/test_project")
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["status"] == "Success"

    # Checking for part data
    response = test_client.get("/part")
    assert response.status_code == 200
    response_json = response.json()
    data_json = json.loads(response_json["data"])
    assert len(data_json) == 0

    # Checking for assembly data
    response = test_client.get("/assembly")
    assert response.status_code == 200
    response_json = response.json()
    data_json = json.loads(response_json["data"])
    assert len(data_json) == 0

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201


def test_get_project(test_client, create_multi_level_assembly):
    """
    GIVEN a FastAPI application
    WHEN the '/project/{project_name}' endpoint is requested (GET)
    THEN check that the response code is valid, and the expected response is returned
    """

    # Saving assembly project
    response = test_client.post("/project/test_project")
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["status"] == "Success"

    # Getting saved assembly project
    response = test_client.get("/project/test_project")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"

    # Checking for part data
    response = test_client.get("/part")
    assert response.status_code == 200
    response_json = response.json()
    data_json = json.loads(response_json["data"])
    assert len(data_json) != 0

    # Checking for assembly data
    response = test_client.get("/assembly")
    assert response.status_code == 200
    response_json = response.json()
    data_json = json.loads(response_json["data"])
    assert len(data_json) != 0

    # Clearing assembly project before other tests
    response = test_client.post("/project/test_project")
    assert response.status_code == 201
