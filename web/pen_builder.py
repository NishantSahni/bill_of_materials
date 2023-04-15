"""
Program to build different types of pens using the Bill of Materials API
"""

from utilities import request_handler as rq


if __name__ == "__main__":
    # Clearing project before starting
    rq.save_assembly_project("base_pen")

    ink_cartridge = ["cartridge_body", "cartridge_cap", "writing_tip"]
    pen_components = ["pocket_clip", "thruster", "spring", "cam"]
    box_parts = ["box_top", "box_bottom", "box_inserts"]

    # Creating parts for base ink cartridge, pen_components & box_parts
    for part in ink_cartridge + pen_components + box_parts:
        rq.add_part(part)

    # Creating base ink cartridge assembly
    rq.add_assembly(assembly_name="ink_cartridge", part_names=ink_cartridge)

    # Creating basic pen assembly
    res = rq.add_assembly(
        assembly_name="pen",
        part_names=pen_components,
        subassembly_names=["ink_cartridge"],
    )

    # Creating pen_box assembly
    response = rq.add_assembly(
        assembly_name="pen_box", part_names=box_parts, subassembly_names=["pen"]
    )

    # Saving basic assembly for re-use
    rq.save_assembly_project("base_pen")
    # Loading a copy of the base assembly
    rq.copy_assembly_project("base_pen")

    barrel_types = ["metal_barrel", "plastic_barrel"]
    ink_colors = ["red_ink", "blue_ink"]

    # Using saved basic assembly to build pen box assemblies with varying materials/colors
    for barrel in barrel_types:
        for ink_color in ink_colors:
            rq.add_part(barrel)
            rq.attach_part_assembly(barrel, "pen")
            rq.add_part(ink_color)
            rq.attach_part_assembly(ink_color, "ink_cartridge")
            project = f"{barrel}_{ink_color}_pen"

            # Displaying each variant of pen assembly
            response = rq.get_assembly("pen_box")

            print(f"{project}:\n")
            rq.render_assembly(response.json()["data"])

            # Saving the current assembly
            rq.save_assembly_project(project)
            # Loading a copy of the base assembly to build more variants
            rq.copy_assembly_project("base_pen")

    rq.save_assembly_project(project)
