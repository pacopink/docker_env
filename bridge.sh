br_name=bridge0
brctl addbr $br_name
ip addr add 192.168.237.10/24 dev $br_name
ip addr del 192.168.237.10/24 dev em1
ip link set $br_name up
brctl addif $br_name ens33
