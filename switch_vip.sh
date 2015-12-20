#!/bin/bash

usage="Usage: switch_vip.sh [container1] [container2] [vip]"


if [ $# != 3 ];then
    echo $usage
    exit -1
else
    container1=$1
    container2=$2
    vip=$3
    brd=`echo ${vip}|perl -ne 'if(/(\d+\.\d+\.\d+)\..*/){printf("$1.255");}'`
fi


if [ "x`docker exec $container1 ip a|grep ${vip}`" != "x" ]; then
    echo "vip in $container1, switch to $container2"
    echo "    removing $vip from $container1"
    vip.sh del $container1 $vip $brd
    echo "    allocating $vip to $container2"
    vip.sh add $container2 $vip $brd
elif [ "x`docker exec $container2 ip a|grep ${vip}`" != "x" ]; then
    echo "vip in $container2, switch to $container1"
    echo "    removing $vip from $container2"
    vip.sh del $container2 $vip $brd
    echo "    allocating $vip to $container1"
    vip.sh add $container1 $vip $brd
else
        echo "vip neither in $container1 nor $container2, allocate to $container1"
        vip.sh add $container1 $vip $brd
fi

#vip.sh del ocg_fe2 192.168.237.190/24 192.168.237.255;vip.sh add ocg_fe1 192.168.237.190/24 192.168.237.255
