#!/bin/env python
import os
from my_fork import *
import sys

if len(sys.argv)<2:
    print "Usage: %s [all|conainter name]"%(sys.argv[0])
    sys.exit(-1)
else:
    to_stop = sys.argv[1:]
    print "to stop %s"%to_stop

# get all running container names
cmd =  'docker ps'
p = os.popen(cmd)
running_lxc = list()
for l in  p.readlines()[1:]:
    running_lxc.append(l.split()[-1])
p.close()
print "Current running lxc %s"%running_lxc


#decide lxc that actually need to stop
actual_stop = list()
if 'all' in to_stop:
    actual_stop = running_lxc
else:
    for i in to_stop:
        if i in running_lxc:
            actual_stop.append(i)
        else:
            print "specified lxc [%s] is not running, not need to stop"%i

#fork stop processes
procs = list()
for i in actual_stop:
    cid = i.split()[-1]
    f = ForkMan(cid)
    f.cmd = "docker stop %s"%cid
    procs.append(f)

for p in procs:
    p.run()

for p in procs:
    print p.status()
    
   



