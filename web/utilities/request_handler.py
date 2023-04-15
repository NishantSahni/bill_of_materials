"""
Handler to handle HTTP requests for interacting with the Bill of Materials API
"""

import logging
import requests
from fastapi import HTTPException
from anytree import RenderTree
from anytree.importer import JsonImporter


# Base URL for APIs
BASE_URL = "http://localhost:8000"
# Request timeout
TIMEOUT = 10


# Logging to file
logging.basicConfig(
    filename="logs/request_handler.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_request(endpoint: str):
    """
    Function to make a GET request to provided endpoint

    Parameters
    ----------
    endpoint : str
        Endpoint for GET request

    Returns
    -------
    Response
        HTTP response object
    """

    try:
        res = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


def post_request(endpoint: str, data: dict | None = None):
    """
    Function to make a POST request to provided endpoint

    Parameters
    ----------
    endpoint : str
        Endpoint for GET request
    data : dict, optional
        Data to post

    Returns
    -------
    Response
        HTTP response object
    """

    try:
        res = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=TIMEOUT)
        if res.status_code not in [200, 201]:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


def put_request(endpoint: str, data: dict | None = None):
    """
    Function to make a PUT request to provided endpoint

    Parameters
    ----------
    endpoint : str
        Endpoint for GET request
    data : dict, optional
        Data to put

    Returns
    -------
    Response
        HTTP response object
    """

    try:
        res = requests.put(f"{BASE_URL}{endpoint}", json=data, timeout=TIMEOUT)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


def delete_request(endpoint: str):
    """
    Function to make a DELETE request to the endpoint

    Parameters
    ----------
    endpoint : str
        Name of endpoint to delete

    Returns
    -------
    Response
        HTTP response object
    """

    try:
        res = requests.delete(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


def get_all_parts():
    """
    Function to make a GET request to the /part endpoint
    to get al parts

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/part")


def get_part(part_name: str):
    """
    Function to make a GET request to the /part/{part_name} endpoint
    to get a part

    Parameters
    ----------
    part_name : str
        Name of part to get

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"part/{part_name}")


def add_part(part_name: str):
    """
    Function to make a POST request to the /part endpoint to create a part

    Parameters
    ----------
    part_name : str
        Name of part to create

    Returns
    -------
    Response
        HTTP response object
    """

    return post_request("/part", {"part_name": part_name})


def delete_part(part_name: str):
    """
    Function to make a DELETE request to the /part/{part_name} endpoint
    to delete a part

    Parameters
    ----------
    part_name : str
        Name of part to delete

    Returns
    -------
    Response
        HTTP response object
    """

    return delete_part(f"/part/{part_name}")


def get_part_ancestors(part_name: str):
    """
    Function to make a GET request to the /part/{part_name}/parents endpoint
    to get a part's ancestors

    Parameters
    ----------
    part_name : str
        Name of part to get ancestors

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/part/{part_name}/parents")


def get_all_assemblies():
    """
    Function to make a GET request to the /assembly endpoint to
    get all assemblies

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/assembly")


def get_assembly(assembly_name: str):
    """
    Function to make a GET request to the /assembly/{assembly_name} endpoint to
    get a specific assembly

    Parameters
    ----------
    assembly_name : str
        Name of assembly to get

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/assembly/{assembly_name}")


def add_assembly(
    assembly_name: str, part_names: list, subassembly_names: list | None = None
):
    """
    Function to make a POST request to the /assembly endpoint to create an assembly

    Parameters
    ----------
    assembly_name : str
        Name of assembly to create
    part_names: list
        List of parts to assemble
    subassembly_names: list, optional
        List of assembly_names to assemble

    Returns
    -------
    Response
        HTTP response object
    """

    post_json = {
        "assembly_name": assembly_name,
        "part_names": part_names,
        "subassembly_names": subassembly_names,
    }
    return post_request("/assembly", post_json)


def attach_part_assembly(part_name: str, assembly_name: str):
    """
    Function to make a POST request to the /assembly/{assembly_name}/child/{part_name}
    endpoint to attach a part to an assembly

    Parameters
    ----------
    part_name : str
        Name of part to attach
    assembly_name: str
        Name of assembly to attach to

    Returns
    -------
    Response
        HTTP response object
    """

    return post_request(f"/assembly/{assembly_name}/child/{part_name}")


def detach_part_assembly(part_name: str, assembly_name: str):
    """
    Function to make a PUT request to the /assembly/{assembly_name}/child/{part_name}
    endpoint to detach a part from an assembly

    Parameters
    ----------
    part_name : str
        Name of part to attach
    assembly_name: str
        Name of assembly to attach to

    Returns
    -------
    Response
        HTTP response object
    """

    return put_request(f"/assembly/{assembly_name}/child/{part_name}")


def get_assembly_first_children(assembly_name: str):
    """
    Function to make a GET request to the /assembly/{assembly_name}/first endpoint to
    get all first-level children of an assembly

    Parameters
    ----------
    assembly_name : str
        Name of assembly to get first-level children from

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/assembly/{assembly_name}/first")


def get_assembly_children(assembly_name: str):
    """
    Function to make a GET request to the /assembly/{assembly_name}/first endpoint to
    get all children of an assembly

    Parameters
    ----------
    assembly_name : str
        Name of assembly to get all children from

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/assembly/{assembly_name}/children")


def get_assembly_leaves(assembly_name: str):
    """
    Function to make a GET request to the /assembly/{assembly_name}/leaves endpoint to
    get all parts in a specific assembly that are not subassemblies

    Parameters
    ----------
    assembly_name : str
        Name of assembly to get all leaves from

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/assembly/{assembly_name}/leaves")


def get_top_assembly():
    """
    Function to make a GET request to the /top_assembly endpoint to
    get all top level assemblies

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/top_assembly")


def get_subassemblies():
    """
    Function to make a GET request to the /subassembly endpoint to
    get all subassemblies

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/subassembly")


def get_component_parts():
    """
    Function to make a GET request to the /component endpoint to
    get all parts that are a part of assemblies

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/component")


def get_orphan_parts():
    """
    Function to make a GET request to the /orphan endpoint to
    get all parts that have no parents or children

    Parameters
    ----------
    None

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request("/orphan")


def save_assembly_project(project_name: str):
    """
    Function to make a POST request to the /project/{project_name} endpoint to
    save an assembly project

    Parameters
    ----------
    project_name : str
        Name of project to save

    Returns
    -------
    Response
        HTTP response object
    """

    return post_request(f"/project/{project_name}")


def copy_assembly_project(project_name: str):
    """
    Function to make a GET request to the /project/{project_name} endpoint to
    copy a saved assembly project

    Parameters
    ----------
    project_name : str
        Name of project to copy

    Returns
    -------
    Response
        HTTP response object
    """

    return get_request(f"/project/{project_name}")


def render_assembly(assembly: str):
    """
    Function to render an assembly to display it in a readable manner

    Parameters
    ----------
    assembly : str
        The assembly json

    Returns
    -------
    None
    """

    try:
        json_importer = JsonImporter()
        root = json_importer.import_(assembly)
        print(RenderTree(root), "\n")
    except Exception as ex:
        logging.exception(ex)
        raise ex
