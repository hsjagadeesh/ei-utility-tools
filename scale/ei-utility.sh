#!/bin/bash

# This utility is to start and stop and check the status of the running containers
# you can start as many containes you want to start or stop
# NUMBER_OF_CONTAINERS >> number of containers you wish to start
# CONTAINERS_RUNNING >> already running containers
# START_CONTAINERS_COUNT >> name counter for container name like ei-local-manager-1, ei-local-manager-2 .... etc
# EXT_PORT >> port number mapped with host from container port
# INT_PORT >> port number of container
# STOP_CONTAINER_NUMBER >> number of containers you wish to stop

SERVICE_NAME="EI Utility Containers"
BUILD_ARGS="-e CAF_SYSTEM_SERIAL_ID=FCW2610Y10Y  -e CAF_SYSTEM_PRODUCT_ID=IR1101-K9  -e CAF_APP_PERSISTENT_DISK_SIZE_KB=256000  -e CAF_APP_LOG_DIR=/data/logs"
IMAGE_NAME="dockerhub-master.cisco.com/iot-darkphoenix-docker/ei-edge-testing:1.16.20"
CONTAINER_NAME="ei-local-manager"
EXT_PORT=8008
INT_PORT=8008
NUMBER_OF_CONTAINERS=$2

CONTAINERS_RUNNING=`docker ps|grep -v NAME | awk '{print $NF}' | wc -l`

start_service() {

    #Check if any containers are running
    echo "Numbers of $SERVICE_NAME already running : " $CONTAINERS_RUNNING

    if [ $CONTAINERS_RUNNING -gt 0 ]; then
	     START_CONTAINERS_COUNT=$((CONTAINERS_RUNNING + 1))
	     echo " $CONTAINERS_RUNNING $SERVICE_NAME are already running.... , Creating new containers from $NEW_CONTAINERS"
    else
	     echo "No $SERVICE_NAME found, starting $2 containers "
	     START_CONTAINERS_COUNT=1
    fi

    echo "Starting $NUMBER_OF_CONTAINERS $SERVICE_NAME..."

    NOC=$NUMBER_OF_CONTAINERS
    CONTAINER_NUMBER=$START_CONTAINERS_COUNT
    EXT_PORT=$((EXT_PORT + $START_CONTAINERS_COUNT))

    for ((i=1; i<=NOC; i++))
    do
       echo "start container $CONTAINER_NAME-$CONTAINER_NUMBER"
       docker run -dit $BUILD_ARGS -p $EXT_PORT:$INT_PORT --name $CONTAINER_NAME-$CONTAINER_NUMBER $IMAGE_NAME
       EXT_PORT=$((EXT_PORT + 1))
       CONTAINER_NUMBER=$((CONTAINER_NUMBER + 1 ))
     done
}

stop_service() {

    if [ $NUMBER_OF_CONTAINERS == "all" ]; then
	      NUMBER_OF_CONTAINERS=$CONTAINERS_RUNNING
	      if  [ $NUMBER_OF_CONTAINERS -eq 0 ]; then
             echo "No $SERVICE_NAME are running"
	      fi
    fi

    COUNTNER=1
    if [ $NUMBER_OF_CONTAINERS -le $CONTAINERS_RUNNING ]; then
	        echo "Stopping $NUMBER_OF_CONTAINERS $SERVICE_NAME..."
	        STOP_CONTAINER_NUMBER=$CONTAINERS_RUNNING
	        while [ $COUNTNER -le $NUMBER_OF_CONTAINERS ]; do
	             echo "stoping and removing $CONTAINER_NAME-$STOP_CONTAINER_NUMBER container....."
               docker stop $CONTAINER_NAME-$STOP_CONTAINER_NUMBER
	             docker rm $CONTAINER_NAME-$STOP_CONTAINER_NUMBER | 2> /dev/null
	             COUNTNER=$((COUNTNER + 1 ))
               STOP_CONTAINER_NUMBER=$((STOP_CONTAINER_NUMBER - 1))
	        done
    elif [ $CONTAINERS_RUNNING -eq 0 ]; then
          echo "No $SERVICE_NAME are running"
    else
	         echo "Number of $SERVICE_NAME running is less then $NUMBER_OF_CONTAINERS"
    fi
}

status_service() {
    echo "Checking status of $SERVICE_NAME..."
    echo "$CONTAINERS_RUNNING $SERVICE_NAME are running...."
}

case "$1" in
    start)
	start_service
        ;;
    stop)
        stop_service
        ;;
    status)
        status_service
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac

exit 0
