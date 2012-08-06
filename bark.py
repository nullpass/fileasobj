#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""

bark.py - If debugg then log string. If unable to log, print.

nullpass, 2012

2012.08.05 - Initial release.

ex:
from bark import bark
bark('hello world')

TODO:
    - if UID is root: logDir = /var/log/
    - clean up imports
    - get rid of debugg, let calling program override (decide) to 
        'import bark' or def bark locally as null-output function.
    
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
        # If unable to load variable 'debugg' assume True
        debugg = True
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
        m = search( '^([a-zA-Z0-9]+)\.*' , os.path.basename(sys.argv[0]) )
        if m:
            thisExec = m.group(1)
        else:
            # Current program doesn't have an extension- so just use it.
            thisExec = os.path.basename(sys.argv[0])
        if len(thisExec) < 3:
            thisExec = 'python'
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
            fileHandle.write(str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+thisProc+" "+str(thisEvent)+'\n')
            fileHandle.close()
        except Exception as thisError:
            #
            # Else print error and event
            # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] [Errno 2] No such file or directory: '/home/me/log/myprogram.log'
            # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] hello world
            print str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+thisProc+" "+str(thisError)
            print str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+thisProc+" "+str(thisEvent)
    return 0
