#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
"""

bark.py - Log given string, if unable to log, print.

nullpass, 2012

2012.08.11 - Convert bark function to class
2012.08.08 - Removed 'debugg' check, leave bark calling up to caller
2012.08.05 - Initial (public) release.

Examples:

# Log 'Hello World' to myapplication.log
from bark import Bark
bark = Bark()
bark.logfile = '/var/log/myapplication.log'
bark.Enabled = True
bark.do('Hello World.')

# Print 'Hello World' in log format
from bark import Bark
bark = Bark()
bark.logfile = False
bark.Enabled = True
bark.do('Hello World.')


TODO:
    - add main() back and allow strings from sys.argv
"""
__version__='3.0.b'
import time
import os
from platform import node
from re import search
import sys

class Bark:
    """
    """
    def __init__(self):
        self.Birthday = (float(time.time()),str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())))
        self.logfile = os.path.expanduser('~')+"/log/"+thisExec+".log"
        self.Enabled = True
        #
        # Try to get base name of current program minus the extension
        m = search( '^([a-zA-Z0-9\-_]+)\.*' , os.path.basename(sys.argv[0]) )
        if m:
            self.thisExec = m.group(1)
        else:
            # Current program doesn't have an extension- so just use it.
            self.thisExec = os.path.basename(sys.argv[0])
        #
        # If the name of the executable is too short or None make it py
        if len(thisExec) < 3:
            self.thisExec = 'python'
        #
        # Hostname
        self.thisHost = node()
        #
        # Current executable and PID
        self.thisProc = self.thisExec+"["+str(os.getpid())+"]"
        #
    def do(self,thisEvent):
        if self.Enabled == True:
            if self.logfile:
                try:
                    #
                    # Try to log event to log file that already exists.
                    self.fileHandle = open(self.logfile, 'a')
                    self.fileHandle.write(str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+self.thisProc+" "+str(self.thisEvent)+'\n')
                    self.fileHandle.close()
                except Exception as self.thisError:
                    #
                    # Else print error and event
                    # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] [Errno 2] No such file or directory: '/home/me/log/myprogram.log'
                    # Sun Aug 05 14:20:37 EDT 2012 myprogram[3125] hello world
                    print str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+self.thisProc+" "+str(self.thisError)
                    print str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+self.thisProc+" "+str(self.thisEvent)
            else:
                print str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+" "+self.thisProc+" "+str(self.thisEvent)
