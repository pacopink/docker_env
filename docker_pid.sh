#!/bin/bash
if [ $# != 1 ];then
    echo "Usage: docker_pid.sh [container_name]"
    exit 1
else
    docker inspect -f "{{.State.Pid}}" $1
fi
