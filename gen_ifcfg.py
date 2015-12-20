#!/bin/env python
import sys

template='''
TYPE=Ethernet
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=no  #disable IPv6
NAME=__NAME__
DEVICE=__NAME__
######################
BOOTPROTO=none
ONBOOT=no
'''
if len(sys.argv)<2:
    print "Usage: gen_ifcfg.py [list of ether itf name]"
    sys.exit(1)

for i in sys.argv[1:]:
    f=open("/etc/sysconfig/network-scripts/ifcfg-%s"%i, "w")
    f.write(template.replace("__NAME__", i))
    f.close()
