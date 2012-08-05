#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""

bark.py - If debugg then log string. If unable to log, print.

nullpass, 2012

ex:
from bark import bark
bark('hello world')

TODO:
    if UID = root then logDir = /var/log/
    clean up imports
    if os.path.basename(sys.argv[0]) is empty, make something up
    
"""

def bark(thisEvent):
    try:
        # 
        # We can't call global variables from inside a module- and to 
        # accept more than 1 argument would defeat the spirit of this
        # module- so try to get the variable 'debugg' from module
        # 'debugg.py' in current directory.
        #
        # The point of the 'debugg' variable is to be able to quickly
        # enable/disable logging program-globally.
        #
        # ./debugg.py contains:
        # debugg = True
        # or
        # debugg = False
        from debugg import debugg
    except:
        #
        # If unable to load variable 'debugg' assume False
        debugg = False
    #
    #
    if debugg == True:
        import time
        import os
        from platform import node
        from re import search
        import sys
        #
        # Try to get base name of current program minus the extension
        m = search( '^([a-zA-Z0-9]+)\.' , os.path.basename(sys.argv[0]) )
        if m:
            #line = line.strip("\n")
            thisExec = m.group(0).strip(".")
        else:
            # Current program doesn't have an extension- so just use it.
            thisExec = os.path.basename(sys.argv[0])
        #
        # Hostname
        thisHost = node()
        #
        # Current executable and PID
        thisProc = thisExec+"["+str(os.getpid())+"]"
        #
        # 
        try:
            #
            # Try to log event
            thisLog = os.path.expanduser('~')+"/log/"+thisExec+".log"
            fileHandle = open(thisLog, 'a')
            fileHandle.write(str(strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+thisProc+" "+str(thisEvent)+'\n')
            fileHandle.close()
        except Exception as thisError:
            #
            # Else print error and event
            # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] [Errno 2] No such file or directory: '/home/me/log/myprogram.log'
            # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] hello world
            print str(strftime("%a %b %d %H:%M:%S %Z %Y", localtime()))+" "+thisProc+" "+str(thisError)
            print str(strftime("%a %b %d %H:%M:%S %Z %Y", localtime()))+" "+thisProc+" "+str(thisEvent)
  return 0
