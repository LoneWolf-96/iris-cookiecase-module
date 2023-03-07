# iris-cookiecase-module
This module is designed for the DFIR IRIS platform to automatically provision notes and note groups when creating a new case.
## Features
- Registers a `on_postload_case_create` hook into IRIS to monitor for new case creation events
- When a new case is created, it will:
    - Read the directory names inside of `/template/` as note groups and the files (do not use extensions) names as note names and their content as default note content

# Creating the module
## Customisation and Building the Module
1. Download the repository and add a directory structure `iris_cookiecase_module/template/<<note_group_name>>/note_name`
2. From the downloaded repository root directory run `make wheel` this will create the wheel package

## Adding the module into IRIS 
1. Copy the `.whl` into both the `iris-web_worker` and the `iris-web_app` docker contains
    * `docker cp '/path/to/wheel/file.whl' iris-web_worker_1:/iriswebapp/dependencies/file.whl`
    * `docker cp '/path/to/wheel/file.whl' iris-web_app_1:/iriswebapp/dependencies/file.whl` 
2. Install the wheel file, using pip3, into each container
    * `docker exec -it iris-web_worker_1 /bin/sh -c "pip3 install /iriswebapp/dependencies/file.whl --force-reinstall"`
    * `docker exec -it iris-web_app_1 /bin/sh -c "pip3 install /iriswebapp/dependencies/file.whl --force-reinstall"`
3. Restart the docker containers
    * `docker restart iris-web-145_app_1`
    * `docker restart iris-web-145_app_1`


# Other Information
* **Licensing Model:** MIT
* **Date Initally Created:** 07-03-2023