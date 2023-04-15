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

    try:
        res = requests.post(
            f"{BASE_URL}/part", json={"part_name": part_name}, timeout=TIMEOUT
        )
        if res.status_code != 201:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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

    try:
        post_json = {
            "assembly_name": assembly_name,
            "part_names": part_names,
            "subassembly_names": subassembly_names,
        }
        res = requests.post(f"{BASE_URL}/assembly", json=post_json, timeout=TIMEOUT)
        if res.status_code != 201:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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

    try:
        res = requests.get(f"{BASE_URL}/assembly/{assembly_name}", timeout=TIMEOUT)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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

    try:
        res = requests.post(f"{BASE_URL}/project/{project_name}", timeout=TIMEOUT)
        if res.status_code != 201:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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

    try:
        res = requests.get(f"{BASE_URL}/project/{project_name}", timeout=TIMEOUT)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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

    try:
        res = requests.post(
            f"{BASE_URL}/assembly/{assembly_name}/child/{part_name}", timeout=TIMEOUT
        )
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, detail=res.json()["detail"]
            )
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


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
