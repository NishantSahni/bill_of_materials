import requests
import logging
from anytree import RenderTree


# Base URL for APIs
BASE_URL = "http://localhost:8000"


# Logging to file
logging.basicConfig(
    filename="logs/pen_builder.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
)


def add_part(part_name: str):
    try:
        response = requests.post(f"{BASE_URL}/part", json={"part_name": part_name})
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


def add_assembly(
    assembly_name: str, part_names: list, subassembly_names: list | None = None
):
    try:
        post_json = {
            "assembly_name": assembly_name,
            "part_names": part_names,
            "subassembly_names": subassembly_names,
        }
        response = requests.post(f"{BASE_URL}/assembly", json=post_json)
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


def get_assembled_components(assembly_name: str):
    try:
        response = requests.get(f"{BASE_URL}/assembly_part")
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


def save_assembly_project(project_name: str):
    try:
        response = requests.post(f"{BASE_URL}/project/{project_name}")
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


def copy_assembly_project(project_name: str):
    try:
        response = requests.get(f"{BASE_URL}/project/{project_name}")
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


def attach_part_assembly(part_name: str, assembly_name: str):
    try:
        response = requests.post(
            f"{BASE_URL}/assembly/{assembly_name}/child/{part_name}"
        )
        return response
    except Exception as ex:
        logging.exception(ex)
        raise ex


if __name__ == "__main__":
    ink_cartridge = ["cartridge_body", "cartridge_cap", "writing_tip"]
    for part in ink_cartridge:
        add_part(part)

    add_assembly(assembly_name="ink_cartridge", part_names=ink_cartridge)

    pen_components = ["pocket_clip", "thruster", "spring", "cam"]
    for part in pen_components:
        add_part(part)

    add_assembly(
        assembly_name="pen",
        part_names=pen_components,
        subassembly_names=["ink_cartridge"],
    )

    box_parts = ["box_top", "box_bottom", "box_inserts"]
    for part in box_parts:
        add_part(part)

    add_assembly(
        assembly_name="pen_box", part_names=box_parts, subassembly_names=["pen"]
    )

    save_assembly_project("base_pen")
    copy_assembly_project("base_pen")

    for material in ["metal_barrel", "plastic_barrel"]:
        add_part(material)
        attach_part_assembly(material, "pen")
        for ink_color in ["red_ink", "blue_ink"]:
            add_part(ink_color)
            attach_part_assembly(ink_color, "ink_cartridge")
            save_assembly_project(f"{material}_{ink_color}_pen")
            response = get_assembled_components("pen_box")
            print(response.json())
            copy_assembly_project("base_pen")
