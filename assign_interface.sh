#!/bin/bash

if [ $# != 4 ]; then
    echo "Usage: assign_itf.sh [container] [eth] [static_ip] [default_gw]"
    echo "Example: assign_itf.sh ocg_dev ens36 192.168.237.99/24 192.168.237.2"
    exit -1
else
    container=$1
    eth=$2
    static_ip=$3
    gw=$4
    echo $container
    echo $eth
    echo $static_ip
#    exit 0
fi

#retrieve the pid of the container
#pid=`docker inspect -f "{{.State.Pid}}" $container`
pid=`docker_pid.sh $container`
#echo $pid

#link to /var/run/netns, ip command will visit this dir
rm -rf /var/run/netns/$pid
mkdir -p /var/run/netns
ln -s /proc/$pid/ns/net /var/run/netns/$pid 

#assign eth interface to container, up the interface in the container and assign ip and default gw
ip link set $2 netns $pid
ip netns exec $pid ip link set $eth up
ip netns exec $pid ip addr add $static_ip dev $eth
ip netns exec $pid ip route add default via $gw

#this is to move out the eth interface out
#ip netns exec 5316 ip link set ens37 netns 1
