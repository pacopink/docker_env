#!/bin/bash

if [ $# != 4 ]; then
    echo "Usage: vip.sh [add|del] [container] [static_ip] [broadcast]"
    echo "Example: vip.sh add ocg_dev 192.168.237.99/24 192.168.237.255"
    exit -1
else
    action=$1
    container=$2
    static_ip=$3
    brd=$4
#    exit 0
fi

eth=`docker exec ${container} ifconfig|perl -ne 'if(/^(ens\d+).*/){print "$1\n";}'`
if [ x$eth = x ]; then
    echo "ERROR: interface not found!!!"
    exit -1
fi

echo $eth

#retrieve the pid of the container
pid=`docker inspect -f "{{.State.Pid}}" $container`
if [ x$pid = x ]; then
    echo "ERROR: cannot find pid from container!!!"
    exit -1
fi

echo $pid

#link to /var/run/netns, ip command will visit this dir
rm -rf /var/run/netns/$pid
mkdir -p /var/run/netns
ln -s /proc/$pid/ns/net /var/run/netns/$pid 

#assign eth interface to container, up the interface in the container and assign ip and default gw
if [ $action = "add" ]; then
    ip netns exec $pid ip addr add $static_ip brd $brd dev $eth #label $label
elif [ $action = "del" ]; then
    ip netns exec $pid ip addr del $static_ip dev $eth
else
    echo "invalid action"
    echo $usage
    exit -1
fi

rm -rf /var/run/netns/$pid
#this is to move out the eth interface out
#ip netns exec 5316 ip link set ens37 netns 1
