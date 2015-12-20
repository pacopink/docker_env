#!/bin/env python
import os
from my_fork import *

cmd =  'docker ps'

p = os.popen(cmd)
l =  p.readlines()[1:]
p.close()
procs = list()
for i in l:
    cid = i.split()[-1]
    f = ForkMan(cid)
    f.cmd = "docker stop %s"%cid
    procs.append(f)


for p in procs:
    p.run()

for p in procs:
    print p.status()
    
    



