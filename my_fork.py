#!/bin/env python

import os
import sys
import  time

SIPP_ERROR_CODE = {    
   0: "All calls were successful",
   1: "At least one call failed",
   97: "Exit on internal command. Calls may have been processed",
   99: "Normal exit without calls processed",
   254: "Fatal error binding a socket",
   255: "Fatal error",
}

def get_str_from_cmd(cmd):
    p = os.popen(cmd)
    strip = p.readline().strip()
    p.close()
    return strip

def get_timestamp(ts=None):
    '''to get the current timestamp in 'YYYYMMDDHHMISS' format'''
    tm = time.localtime(ts)
    return "%04d-%02d-%02d %02d:%02d:%02d"%(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)

class ForkMan(object):
    def __init__(self, label):
        self.pid = 0
        self.cmd = "ls"
        self.label = label

    def run(self):
        p = os.fork()
        if p!=0:
            self.pid = p
            print "%s %s : child pid [%d]"%(get_timestamp(), self.label, self.pid)
        else:
            print "%s %s Run: [%s] in child process"%(get_timestamp(), self.label, self.cmd)
            #cc = self.cmd.split(' ')
            #print cc
            #x = os.execl(cc[0], *cc[1:])/256
            x = os.system(self.cmd)/256

            try:
                print "%s %s exit with code[%d]: %s"%(get_timestamp(), self.label, x, SIPP_ERROR_CODE[x])
            except:
                print "%s %s exit with undefined code[%d]"%(get_timestamp(), self.label, x)
    
            sys.exit(x)

    def status(self):
        try:
            return os.waitpid(self.pid, os.WNOHANG)
        except OSError, e:
            print "state Exception: %s"%e
            print "errno [%d]"%e.errno
            if e.errno == 10:
                return (self.pid, 0)
                

    def check_status(self, p, s):
        if p == 0:
            return
        if s>256:
            print "%s %s pid[%d] exit with code[%d]"%(get_timestamp(), self.label, p, s/256)
        elif s == 0:
            print "%s %s pid[%d] exit normally"%(get_timestamp(), self.label, p)
        else:
            print "%s %s pid[%d] exit with signal[%d]"%(get_timestamp(), self.label, p, s)

    def stop(self):
        if self.pid > 0:
            os.kill(self.pid, 9)
            self.check_status( *os.waitpid(self.pid, 0) )

class UAC(ForkMan):
    def __init__(self, prog="sipp", xml="uas.xml", rhost="127.0.0.1", rport=5069, inf="", debug=False):
        super(UAC, self).__init__("UAC")
        #only retransmission for 2 times
        options = ""
        if not debug:
            options = ">/dev/null 2>&1"
        self.cmd = "%s -sf %s -r 1 -m 1 -max_retrans 2 %s %s:%d %s"%(prog, xml, inf, rhost, rport, options)
        #self.cmd = "%s -sf %s -r 1 -m 1 -max_retrans 2 %s:%d"%(prog, xml, rhost, rport) 
        self.pid = 0
        self.housekeep_cmd = 'ps -e -o "%%p %%a"|grep " %s:%d"|grep -v grep|perl -ne \'if(/\\s*(\\d+)\\s*.*/){print $1,"\\n";}\'|xargs kill -9>/dev/null 2>&1'%(rhost, rport)
        os.system(self.housekeep_cmd)
        #print self.housekeep_cmd
    def stop(self):
        if self.pid > 0:
            os.system(self.housekeep_cmd) #harvest subprocesses
            os.kill(self.pid, 9)
            self.check_status( *os.waitpid(self.pid, 0) )

class UAS(ForkMan):
    def __init__(self, prog="sipp", xml="uas.xml", lport=5069, inf=""):
        super(UAS, self).__init__("UAS")
        self.cmd = "%s -sf %s -p %d %s>/dev/null 2>&1"%(prog, xml, lport, inf)
        self.pid = 0
        self.housekeep_cmd = 'ps -e -o "%%p %%a"|grep "\\-p %d"|grep -v grep|perl -ne \'if(/\\s*(\\d+)\\s*.*/){print $1,"\\n";}\'|xargs kill -9 >/dev/null 2>&1'%lport
        os.system(self.housekeep_cmd)
        #print self.housekeep_cmd
    def stop(self):
        if self.pid > 0:
            os.system(self.housekeep_cmd) #harvest subprocesses
            os.kill(self.pid, 9)
            self.check_status( *os.waitpid(self.pid, 0) )
    
            

if __name__=="__main__":
    TIMEOUT=10
    uas = UAS("/usr/local/bin/sipp",xml="/ocg/uas.xml", lport=5077)
    uac = UAC("/usr/local/bin/sipp", "/ocg/uac.xml", "127.0.0.1", 5077)
    uas.run()
    time.sleep(0.5)
    (p, s) = uas.status()
    if p!=0:
        print "UAS failed to start"
        uas.check_status(p, s)
        sys.exit(1)
    print "UAS started, kick off UAC ..."

    uac.run()
    t = 0
    t0 = time.time()
    while True:
        now = time.time()
        if now - t >= 0.5:
            t = now
            (p, s) = uac.status()
            uac.check_status(p, s)
            if p>0:
                break
        if now - t0 > TIMEOUT:
            print "UAC wait result timeout after [%d] seconds"%(TIMEOUT)
            uac.stop()
            break
    uas.stop()
