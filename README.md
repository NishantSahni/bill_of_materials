Bill Of Materials (BOM) API
===

This API is used to make [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) requests against Bill of Materials (BOMs).

To run this application, one should only need [Docker](https://docs.docker.com/get-started/overview/) installed and running. The BOM API runs within a container - and instructions for running the application can be found in the [Running](#Running) section of this README.

This application uses FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI has a dedicated website for [documentation](https://fastapi.tiangolo.com/tutorial/).

The main code for the application is contained within the [app.py](web/app.py) file. The tests are all contained within the [tests](tests) directory.

The logs are stored in the web/logs directory.

Feel free to restructure the directory as desired.

Application Structure
---

<!--This section contains a short description of the application structure-->

The RESTful APIs built using FastAPI reside in the web/app.py file.

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


Testing
---

<!--This section contains instructions for running the automated tests for the application-->


The following commands, from within this README's directory, will run tests for the application:
```shell script
$ docker-compose -f "docker-compose.yml" exec web "python3" "-m" "pytest"
```
> Note: The container for the app needs to be running for this command to work. To ensure the container is running, run `docker ps` to show all running containers.