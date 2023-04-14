Coding Challenge: RESTful Bills Of Materials
===

Please aim to spend no more than 4-6 hours on this assignment, with the goal of giving us a read on your skill crafting a small, [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) web service and packaging a deliverable for fellow engineers.

We prefer that you submit a RESTful API using the Python Flask framework, but your alternate option is to use C#.

Your solution is *not* required to persist data between restarts.

Please provide instructions to build, run, and test the service you create. We will evaluate your submission based on correctness, structure and clarity of your code, configuration and communication, and how the deliverable itself is packaged for review. Questions, including meta-feedback on the assignment, are welcome at <swe-coding-submission@silanano.com>.

Thanks in advance!


-------------------


A manufactured product may be described with a Bill of Materials (a list of physical parts, often abbreviated as a BoM). For example, a typical retractable ballpoint pen consists of a:
- barrel bottom
- barrel top
- pocket clip (usually assembled onto the barrel top)
- a thruster (the part you push with your thumb)
- a cam (the part that locks down/up when the thruster is depressed)
- in some cases, a rubber grip (usually assembled onto the barrel bottom)
- spring
- ink cartridge, which may consist of...
   - cartridge body
   - cartridge cap
   - writing tip
   - ink
- a complete pen may be put into a package that includes...
   - pen
   - box top
   - box bottom
   - box insert (which holds the pen)

Some parts may come in different colors (e.g. red, blue, black) to match the color of the ink in the cartridge, but different colors of pen may also use the same part (e.g. the spring). Different models of pen may use different parts for the same function (e.g. one model may have a plastic barrel, another may have a metal barrel). 

In addition, some of the parts are put together into subassemblies before they are put into a final assembly. For example, the pocket clip is attached to the top barrel to create a top barrel assembly, and then the top barrel assembly is assembled with the rest of the parts to make a pen assembly. The pen assembly and top barrel assembly are generally tracked as separate parts that contain their component parts and subassemblies.

The challenge is to implement a JSON-based REST API to create, update, delete and query bills of materials. The implemented API should be addressable with an HTTP client like curl, wget or Postman. Functionality should be provided to:
- create a new part
- add one or more parts as "children" to a "parent" part, which then becomes an assembly
- remove one or more parts from an assembly
- delete a part (thereby also deleting the part from its parent assemblies)
- list all parts
- list all assemblies
- list all top level assemblies (assemblies that are not children of another assembly)
- list all subassemblies (assemblies that are children of another assembly)
- list all component parts (parts that are not subassemblies, but are included in a parent assembly)
- list all orphan parts (parts with neither parents nor children)
- list all the first-level children of a specific assembly
- list all children of a specific assembly
- list all parts in a specific assembly (which are not subassemblies)
- list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly)

Provide code and associated sample data to instantiate and query several varieties of pen:
- two different models of pen (e.g. metal barrel & plastic barrel)
- two different colors of each model (e.g. red, blue, black)

As a bonus, describe and implement an enhancement of your choosing to improve robustness, performance and/or functionality of the service.
