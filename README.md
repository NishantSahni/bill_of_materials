Bill Of Materials (BOM) API
===

This API is used to make [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) requests against Bill of Materials (BOMs).

To run this application, one should only need [Docker](https://docs.docker.com/get-started/overview/) installed and running. The BOM API runs within a container - and instructions for running the application can be found in the [Running](#Running) section of this README.

This application uses FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI has a dedicated website for [documentation](https://fastapi.tiangolo.com/tutorial/).

The main code for the application is contained within the [app.py](web/app.py) file. The tests are all contained within the [tests](tests) directory.

The API & Pen Builder logs are stored in the [logs](web/logs) directory.


Application Structure
---

<!--This section contains a short description of the application structure-->

Due to the heirarchial nature of the problem statement, the data structure used to represent the parent/child relationship is a n-ary tree implemented using AnyTree. Here each tree node has a parent attribute to reference its parent and a children attribute, which is a tuple, with references to all of its children. For more info on the data structure, you can refer its [documentation](https://anytree.readthedocs.io/en/latest/).

Typical usage of the APIs would be as follows:
1. Create parts by posting to the /part endpoint with the part name.
2. Create assemblies by posting to the /assembly endpoint with the assembly name, list of part names to be assembled, and an optional list of subassemblies to be assembled.
3. You can save the assembly project by posting to the /project endpoint with the project name, which will also clear the current project so you can start building a new assembly project right away.
4. You can load copies of saved projects through a get request on the /project endpoint with the project name. This is especially useful when you want to re-use base assembled components, and add variations of parts (materials/color).

Some bonus enhancements:
1. Swapped Flask with FastAPI for much faster asynchronous REST APIs
2. More comprehensive OpenAPI documentation available at http://localhost:8000/docs
3. Added logging to log API server errors to the web/logs/app.log file
4. Added additional functionality to APIs that allows for working on multiple assembly projects
5. Added APIs to attach & detach parts to/from existing assemblies

The Bill of Materials RESTful APIs built using FastAPI reside in the [app.py](web/app.py) file.

The Pen Builder code resides in the [pen_builder.py](web/pen_builder.py) file.

The request handler code to interact with the BOM APIs resides in [request_handler.py](web/utilities/request_handler.py)

The pytest fixtures reside in the [conftest.py](web/tests/conftest.py) file.

The pytest unit tests reside in the [test_app.py](web/tests/functional/test_app.py) file.


Endpoints
---

<!--This section contains endpoints that are reachable when the application is running-->

To view detailed OpenAPI documentation for the APIs go to: http://localhost:8000/docs after running the application with the instructions below.

Running
---

<!--This section contains instructions for running the application-->

The following commands, from within this README's directory, will run the application:
```shell script
$ docker-compose -f "docker-compose.yml" up -d --build
```

Once up and running, the health page for the application can be retrieved at http://localhost:8000/health

The following commands, from within this README's directory, will run the Pen Builder code for the application that uses the APIs:
```shell script
$ docker-compose -f "docker-compose.yml" exec web "python3" "-m" "pen_builder"
```
> Note: The container for the app needs to be running for this command to work. To ensure the container is running, run `docker ps` to show all running containers.

Testing
---

<!--This section contains instructions for running the automated tests for the application-->


The following commands, from within this README's directory, will run tests for the application:
```shell script
$ docker-compose -f "docker-compose.yml" exec web "python3" "-m" "pytest"
```
> Note: The container for the app needs to be running for this command to work. To ensure the container is running, run `docker ps` to show all running containers.
