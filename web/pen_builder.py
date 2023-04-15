"""
Program to build different types of pens using the Bill of Materials API
"""

import logging
import requests
from anytree import RenderTree
from anytree.importer import JsonImporter


# Base URL for APIs
BASE_URL = "http://localhost:8000"
# Request timeout
TIMEOUT = 10


# Logging to file
logging.basicConfig(
    filename="logs/pen_builder.log",
    filemode="a",
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
        return res
    except Exception as ex:
        logging.exception(ex)
        raise ex


if __name__ == "__main__":
    # Creating parts for base ink cartridge
    ink_cartridge = ["cartridge_body", "cartridge_cap", "writing_tip"]
    for part in ink_cartridge:
        add_part(part)

    # Creating base ink cartridge assembly
    add_assembly(assembly_name="ink_cartridge", part_names=ink_cartridge)

    # Creating parts for basic pen
    pen_components = ["pocket_clip", "thruster", "spring", "cam"]
    for part in pen_components:
        add_part(part)

    # Creating basic pen assembly
    add_assembly(
        assembly_name="pen",
        part_names=pen_components,
        subassembly_names=["ink_cartridge"],
    )

    # Creating parts for pen box assembly
    box_parts = ["box_top", "box_bottom", "box_inserts"]
    for part in box_parts:
        add_part(part)

    # Creating pen_box assembly
    add_assembly(
        assembly_name="pen_box", part_names=box_parts, subassembly_names=["pen"]
    )

    # Saving basic assembly for re-use
    save_assembly_project("base_pen")
    copy_assembly_project("base_pen")

    barrel_types = ["metal_barrel", "plastic_barrel"]
    ink_colors = ["red_ink", "blue_ink"]

    json_importer = JsonImporter()

    # Using saved basic assembly to build pen box assemblies with varying materials/colors
    for barrel in barrel_types:
        for ink_color in ink_colors:
            add_part(barrel)
            attach_part_assembly(barrel, "pen")
            add_part(ink_color)
            attach_part_assembly(ink_color, "ink_cartridge")
            project = f"{barrel}_{ink_color}_pen"

            # Displaying each variant of pen assembly
            response = get_assembly("pen_box")
            pen_box_root = json_importer.import_(response.json()["data"])
            print(f"{project}:\n")
            print(RenderTree(pen_box_root), "\n")

            save_assembly_project(project)
            copy_assembly_project("base_pen")

    save_assembly_project(project)
