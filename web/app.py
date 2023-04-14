"""
This file contains the main application code
"""

import json
import logging
import copy
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anytree import AnyNode
from anytree.exporter import JsonExporter


class PartModel(BaseModel):
    """
    Data model for POST part API
    """

    part_name: str


class AssemblyModel(BaseModel):
    """
    Data model for POST assembly API
    """

    assembly_name: str
    part_names: list
    subassembly_names: list | None = None


# Key-Value pairs of all part names with their corresponding objects
gParts = {}
# Key-Value pairs of all assembly names with their corresponding objects
gAssemblies = {}
# Key-value pair of all top level assembly names with their corresponding objects
gAssembly_parts = {}
# Dictionary to store assembly projects
gProjects = {}

# To export anytree to JSON
exporter = JsonExporter(sort_keys=True)
# Logging to file
logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
)


app = FastAPI()


@app.get("/")
async def hello_world():
    """
    GET endpoint that returns hello world
    """

    return {"data": "Hello, World"}


@app.get("/health")
async def get_health():
    """
    GET endpoint that returns health
    """

    return {"status": "Running"}


@app.get("/part", status_code=200)
async def get_part():
    """
    GET endpoint that returns all created parts
    """

    try:
        result = []
        for item in gParts.values():
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/part/{part_name}", status_code=200)
async def get_part_by_name(part_name: str):
    """
    GET endpoint that returns a specific part based on part_name
    """

    try:
        return {
            "status": "Success",
            "data": exporter.export(gParts[part_name]) if part_name in gParts else None,
        }
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.post("/part", status_code=201)
async def post_part(part: PartModel):
    """
    POST endpoint that creates a new part
    """

    try:
        if part.part_name not in gParts:
            # Creates a new node for the part
            gParts[part.part_name] = AnyNode(id=part.part_name)
            return {
                "status": "Success",
                "message": "Part Created",
                "data": exporter.export(gParts[part.part_name]),
            }
        raise HTTPException(status_code=403, detail="Part exists")
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.delete("/part/{part_name}", status_code=200)
async def delete_part(part_name: str):
    """
    DELETE endpoint that deletes a part by part_name
    """

    try:
        # Checking if no parts created or part_name provided not created
        if not gParts or part_name not in gParts:
            raise HTTPException(status_code=403, detail="Part not created")
        # Detaching part from parent before deleting
        gParts[part_name].parent = None
        del gParts[part_name]
        return {"status": "Success", "message": "Part deleted"}
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/part/{part_name}/parents", status_code=200)
async def get_part_ancestors(part_name: str):
    """
    GET endpoint that returns all assemblies that contain a specific child part
    """

    try:
        result = []
        # Getting all ancestors (assemblies) of specified child part
        part_ancestors = gParts[part_name].ancestors
        for item in part_ancestors:
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly", status_code=200)
async def get_assembly():
    """
    GET endpoint that returns all assemblies
    """

    try:
        result = []
        for item in gAssemblies.values():
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly/{assembly_name}", status_code=200)
async def get_assembly_by_name(assembly_name: str):
    """
    GET endpoint that gets a specific assembly based on assembly_name
    """

    try:
        # Checking if no assemblies created or if assembly_name provided not created
        if not gAssemblies or assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly not created")
        return {
            "status": "Success",
            "data": exporter.export(gAssemblies[assembly_name])
            if assembly_name in gAssemblies
            else None,
        }
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.post("/assembly", status_code=201)
async def post_assembly(assembly: AssemblyModel):
    """
    POST endpoint that creates a new assembly
    """

    try:
        # Checking if any parts created
        if not gParts:
            raise HTTPException(status_code=403, detail="No parts created")
        for part_name in assembly.part_names:
            # Checking if the child part is created
            if part_name not in gParts:
                raise HTTPException(
                    status_code=404, detail=f"Part name {part_name} doesn't exist"
                )
            # Checking if the child part already has a parent
            if gParts[part_name].parent:
                raise HTTPException(
                    status_code=403,
                    detail=f"Part name {part_name} already has a parent",
                )

        new_assembly = AnyNode(id=assembly.assembly_name)
        # Attaching child parts to new assembly
        for part_name in assembly.part_names:
            gParts[part_name].parent = new_assembly

        if assembly.subassembly_names:
            # Checking if any assemblies created
            if not gAssemblies:
                raise HTTPException(status_code=403, detail="No assemblies created")
            for subassembly_name in assembly.subassembly_names:
                # Checking if child subassembly is created
                if subassembly_name not in gAssemblies:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Assembly name {subassembly_name} doesn't exist",
                    )
                # Checking if child subassembly already has a parent
                if gAssemblies[subassembly_name].parent:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Assembly name {subassembly_name} already has a parent",
                    )
            # Attaching child assemblies to new assembly
            for subassembly_name in assembly.subassembly_names:
                del gAssembly_parts[subassembly_name]
                gAssemblies[subassembly_name].parent = new_assembly

        # Adding new assembly to top-level assembly and assembly data stores
        gAssembly_parts[assembly.assembly_name] = new_assembly
        gAssemblies[assembly.assembly_name] = new_assembly
        return {
            "status": "Success",
            "message": "Assembly Created",
            "data": exporter.export(new_assembly),
        }
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.put("/assembly/{assembly_name}/child/{part_name}", status_code=200)
async def detach_part_assembly(assembly_name: str, part_name: str):
    """
    PUT endpoint that detaches part_names from assembly
    """

    try:
        if not gParts:
            raise HTTPException(status_code=403, detail="No parts created")
        if assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly name doesn't exist")
        # Checking if part_name exists and its parent is assembly_name
        if part_name in gParts and gParts[part_name].parent.id == assembly_name:
            # Detaching part_name from parent assembly
            gParts[part_name].parent = None
        else:
            raise HTTPException(
                status_code=403, detail="Part name provided not in assembly"
            )
        return {
            "status": "Success",
            "message": "Assembly parts removed",
            "data": exporter.export(gAssemblies[assembly_name]),
        }
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.post("/assembly/{assembly_name}/child/{part_name}", status_code=200)
async def attach_part_assembly(assembly_name: str, part_name: str):
    """
    POST endpoint that attaches part_names to assembly
    """

    try:
        if not gParts:
            raise HTTPException(status_code=403, detail="No parts created")
        if assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly name doesn't exist")
        # Checking if part_name exists and is an orphan
        if part_name in gParts and not gParts[part_name].parent:
            # Attaching part_name to parent assembly
            gParts[part_name].parent = gAssemblies[assembly_name]
        else:
            raise HTTPException(status_code=403, detail="Part name provided has parent")
        return {
            "status": "Success",
            "message": "Assembly parts attached",
            "data": exporter.export(gAssemblies[assembly_name]),
        }
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly/{assembly_name}/first", status_code=200)
async def get_assembly_first_level_children(assembly_name: str):
    """
    GET endpoint that returns first level children of specific assembly
    """

    try:
        result = []
        # Checking if specified assembly exists
        if assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly name not created")
        # Getting first level children of specified assembly
        assembly_children = gAssemblies[assembly_name].children
        for item in assembly_children:
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly/{assembly_name}/children", status_code=200)
async def get_assembly_children(assembly_name: str):
    """
    GET endpoint that returns all children of specific assembly
    """

    try:
        result = []
        # Checking if specified assembly exists
        if assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly name not created")
        # Getting all descendants (children) of specified assembly
        assembly_children = gAssemblies[assembly_name].descendants
        for item in assembly_children:
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly/{assembly_name}/leaves", status_code=200)
async def get_assembly_leaves(assembly_name: str):
    """
    GET endpoint that returns all parts in a specific assembly that are not subassemblies
    """

    try:
        result = []
        # Checking if specified assembly exists
        if assembly_name not in gAssemblies:
            raise HTTPException(status_code=403, detail="Assembly name not created")
        # Getting all leaves (parts with no children) for specified assembly
        assembly_children = gAssemblies[assembly_name].leaves
        for item in assembly_children:
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/assembly_part", status_code=200)
async def get_assembly():
    """
    GET endpoint that returns all assemblies
    """

    try:
        result = []
        for item in gAssembly_parts.values():
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/top_assembly", status_code=200)
async def top_assembly():
    """
    GET endpoint that returns all top level assemblies
    """

    try:
        result = []
        for item in gAssembly_parts.values():
            result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/subassembly", status_code=200)
async def get_subassembly():
    """
    GET endpoint that returns all subassemblies
    """

    try:
        result = []
        # Getting all assemblies with parents
        for item in gAssemblies.values():
            if item.parent:
                result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/component", status_code=200)
async def get_component_part():
    """
    GET endpoint that returns component parts
    """

    try:
        result = []
        # Getting all parts with parents
        for item in gParts.values():
            if item.parent:
                result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/orphan", status_code=200)
async def get_orphan_part():
    """
    GET endpoint that returns orphan parts
    """

    try:
        result = []
        # Getting all parts that don't have any parents or children
        for item in gParts.values():
            if not item.parent and not item.children:
                result.append(exporter.export(item))
        return {"status": "Success", "data": json.dumps(result)}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.get("/project/{project_name}", status_code=200)
async def get_project(project_name: str):
    """
    GET endpoint that returns a copy of saved assembly projects
    """

    try:
        if project_name not in gProjects:
            raise HTTPException(status_code=404, detail="Project name does not exist")

        global gParts, gAssemblies, gAssembly_parts

        # Getting a copy of saved assembly projects
        gParts, gAssemblies, gAssembly_parts = (
            copy.deepcopy(gProjects[project_name]["gParts"]),
            copy.deepcopy(gProjects[project_name]["gAssemblies"]),
            copy.deepcopy(gProjects[project_name]["gAssembly_parts"]),
        )
        return {"status": "Success", "message": "Project copied"}
    except Exception as ex:
        logging.exception(ex)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(status_code=500, detail=str(ex)) from ex


@app.post("/project/{project_name}", status_code=201)
async def post_project(project_name: str):
    """
    POST endpoint that saves an assembly project
    """

    try:
        global gParts, gAssemblies, gAssembly_parts

        # Saving assembly project
        gProjects[project_name] = {
            "gParts": gParts,
            "gAssemblies": gAssemblies,
            "gAssembly_parts": gAssembly_parts,
        }
        gParts, gAssemblies, gAssembly_parts = {}, {}, {}
        return {"status": "Success", "message": "Project saved"}
    except Exception as ex:
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=str(ex)) from ex


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
