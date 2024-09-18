# EI Utility Tools

This repo contains tools related to EI Local Manager 

## EI-CLI

TODO : Steps to use ei-cli tool

## Scale Infrastructure

### EI Utility Containers Script

*This script is used to manage Docker containers by providing options to start, stop, or check the status of running EI Utility Containers. It allows you to specify the number of containers to start or stop, and maps container ports dynamically based on user input.*

## Features
* **Start Containers:** Start a specified number of containers using a custom image and environment variables.
* **Stop Containers:** Stop a specified number of running containers or stop all of them.
* **Check Status:** Display how many containers are currently running.
* **Port Mapping:** Automatically map container ports starting from a base external port.

## Prerequisites
* Docker installed and running.
* Sufficient resources (memory, CPU) to run multiple containers.

## Variables
|Variable Name	|Description |
|---------------|------------|
|SERVICE_NAME	|Descriptive name of the service (in this case, "EI Utility Containers").
|BUILD_ARGS	|Arguments passed when creating containers, including environment variables.
|IMAGE_NAME	|Docker image to use for creating containers (default: dockerhub-master.cisco.com/iot-darkphoenix-docker/ei-edge-testing:1.16.20).
|CONTAINER_NAME	|Base name of containers (e.g., ei-local-manager-1).
|EXT_PORT	|Base external port for mapping container ports to host ports (default: 9000).
|INT_PORT	|Internal port used within the containers (default: 8008).
|NUMBER_OF_CONTAINERS	|Number of containers to start or stop.
|CONTAINERS_RUNNING	|Number of containers that are currently running.
|NAME_OF_CONTAINERS_RUNNING	|Retrieves the name of running containers.
|START_CONTAINERS_COUNT	|Name counter for the containers, used to uniquely name them when creating.

## Usage
# Start Containers #
* To start a specified number of containers:

```bash
sh ei-container.sh start <number_of_containers>
```
For example, to start 5 containers:
```bash
sh ei-container.sh start 5
```
## Stop Containers ##

* To stop a specified number of containers:

```bash
sh ei-container.sh stop <number_of_containers>
```
* For example, to stop 3 containers:

```bash
sh ei-container.sh stop 3
```
* To stop all running containers:

```bash
sh ei-container.sh stop all
```
## Check Status ##
* To check the status of running containers:

```bash
sh ei-container.sh status
```
## This will display the number of containers currently running. ##

## Error Handling
If the required arguments are not provided for the start or stop commands, the script will display an error message like this:

```bash
========= Incomplete Arguments, Both arguments must be provided  =========
Exp:- sh ei-container.sh start 10|20
```

Similarly, when stopping containers, the script will ensure that the number of containers provided is not greater than the number of currently running containers.

### Example ##
Starting 3 containers with the default configuration:

```bash
sh ei-container.sh start 3
```

Stopping 2 containers:

```bash
sh ei-container.sh stop 2
```

Checking the status of containers:

```bash
sh ei-container.sh status
```
## Notes ##
* The script dynamically assigns external ports starting from the base port 9000. Each new container will map the next available port, incrementing by 1.
* Ensure you have sufficient resources to run the specified number of containers, especially when using a high number.
