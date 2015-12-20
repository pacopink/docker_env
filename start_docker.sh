#!/bin/bash


if [ $# != 4 ]; then
    echo "Usage: start_docker.sh [container] [eth] [static_ip] [default_gw]"
    echo "Example: start_docker.sh ocg_dev ens36 192.168.237.99/24 192.168.237.2"
    exit -1
else
    container=$1
    dev=$2
    ip=$3
    gw=$4
fi

docker start $container
assign_interface.sh $container $dev $ip $gw
docker exec $container ifconfig
docker exec $container service sshd start



