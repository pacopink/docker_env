#!/bin/env python

import my_containers
from my_fork import *
import sys

if len(sys.argv)<2:
    print "Usage: %s [all|conainter name]"%(sys.argv[0])
    sys.exit(-1)
else:
    to_start = sys.argv[1:]
    print "to start %s"%to_start

cfg = my_containers.my_containers

cmd =  'docker ps -a'
p = os.popen(cmd)
all_lxc = list()
for l in  p.readlines()[1:]:
    all_lxc.append(l.split()[-1])
p.close()

procs = list()
for i in cfg:
    if to_start[0] == 'all' or i['name'] in to_start: #all or the name in the list, try to start it up
        if i['name'] not in all_lxc:
            print "WARNING: lxc [%s] not exist."%i['name']
            continue
        f = ForkMan(i['name'])
        f.cmd = 'start_docker.sh %s %s %s %s'%(i['name'], i['dev'], i['ip'], i['gw'])
        #print cmd
        procs.append(f)

for p in procs:
    p.run()

for p in procs:
    print p.status()
   
