#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
npnlocker.py - Provide easy lock file management as a class

nullpass, 2012

2012.08.xx - Initial release

Logic:
    If lock file exists but proc not running: OK, overwrite
    If lock file does not exist: OK, create
    If lock file exists but is older than X: OK, kill pid and overwrite
    If lock file exists and proc running: FAIL
    

Example:

# Try to create a lock file using a custom pid file, don't allow a 
# previous instance to be killed, let it run as an orphan.
# Set maximum age of the lock file to be 999999999 seconds.

from npnlocker import Locker
mylock = Locker()
mylock.lockfile = '/var/run/custom.pid'
mylock.maxage = int(999999999)
mylock.Killable = False
if mylock.create():
    print 'I made a lock file'
    print 'Debugg output: \n'+str(mylock.Trace)
else:
    print 'unable to create lock file'
    print 'Errors: \n'+str(mylock.Errors)

"""
  
__version__ = '0.0.b'
import time
import os
from platform import node
from re import search
import sys

class Locker:
    """
    """
    def __init__(self):
        """
        """
        self.Birthday = (float(time.time()),str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())))
        self.Enabled = True
        self.Killable = True # Allow/Deny Locker() from killing old (stuck) processes matching this application.
        #
        # List of any exceptions caught
        self.Errors = []
        #
        # String containing information about steps taken. Used for debugging
        #>>> print m.Trace
        #check
        #pid file found
        #get old pid
        #pid running
        #get command of old pid
        #delete
        #create
        self.Trace = ''
        #
        # Max age (in seconds) a lock file can be before it's considered invalid
        self.maxage = int(300) 
        #
        # Name of file this is running as
        self.thisExec = str(os.path.basename(sys.argv[0]))
        if len(self.thisExec) < 3 or len(self.thisExec) > 255:
            #
            # If there's no name in argv[0], like if you call this from 
            # the Python shell, call this python_$$
            # Also catches names too short or long.
            self.thisExec = 'python_'+str(os.getpid())
        #
        # Hostname
        self.thisHost = node()
        #
        # Current executable and PID, like myapp[12345]
        self.thisProc = self.thisExec.rstrip('.py')+"["+str(os.getpid())+"]"
        #
        # Full path to lock file, default to var/run/thisExec.pid
        self.lockfile = '/var/run/'+self.thisExec+'.pid'
        #
        # Alias remove to delete, for easier use.
        # mylock.remove() and mylock.delete() do the same thing
        self.remove = self.delete
    def __log(self,thisEvent):
        self.Trace += str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+' '+self.thisProc+' '+str(thisEvent)+'\n'
        return
    def create(self):
        """
        check() for existing lock file, if that returns True create a 
        new lock file and return True.
        """
        self.__log('create(self)')
        if self.check():
            try:
                fileHandle = open(self.lockfile, 'w')
                fileHandle.write(str(os.getpid()) + '\n')
                fileHandle.close()
                return True
            except Exception as e:
                self.Errors.append(e)
        return False
    def delete(self):
        """
        Remove the lock file. 
        This can also be accessed as mylock.remove()
        """
        self.__log('delete(self)')
        try:
            os.remove(self.lockfile)
            return True
        except Exception as e:
            self.Errors.append(e)
        return False
    def check(self):
        """
        Check for lock file, running proc, and name of running proc.
        """
        self.__log('check(self)')
        if os.path.exists(self.lockfile):
            #
            # Lock file already exists, see if prev proc still running.
            self.__log('PID file '+str(self.lockfile)+' found')
            try:
                #
                # Get PID inside current lock file
                self.__log('Get old PID from '+str(self.lockfile))
                fileHandle = open(self.lockfile, 'r')
                self.oldpid = fileHandle.read().rstrip()
                fileHandle.close()
                if os.path.exists( '/proc/'+str(self.oldpid) ):
                    self.__log('PID '+str(self.oldpid)+' is running, check name in /proc/%s/cmdline')
                    if os.path.exists( '/proc/'+str(self.oldpid)+'/cmdline' ):
                        self.__log('Get the command and arguments in cmdline as a string')
                        fileHandle = open('/proc/'+str(self.oldpid)+'/cmdline', 'r')
                        currentProc = fileHandle.read()
                        fileHandle.close()
                        if self.thisExec in currentProc:
                            self.__log('Proc running as self.oldpid looks like an instance of this program.')
                            self.__log(currentProc)
                            self.__log('Check the age of the lock file')
                            mtimeOfFile = int(os.path.getmtime(self.lockfile))
                            currTime = int(time.time())
                            timeDiff = currTime - mtimeOfFile
                            if timeDiff > self.maxage:
                                #
                                # The difference in time between now and
                                # the last time the existing lock file 
                                # was modified is MORE than the threshold
                                # defined as self.maxage
                                # 
                                # Try to kill the old PID
                                self.__log('lock file too old, timeDiff='+str(timeDiff))
                                if self.murder():
                                    return True
                                return False
                            if timeDiff < self.maxage:
                                #
                                # Lock file created recently, PID still
                                # running and the process looks like 
                                # this application, refuse new lock.
                                self.__log('lock file recently modofied, timeDiff='+str(timeDiff))
                                return False
                        else:
                            #
                            # Proc matching PID in lock file is not this
                            # application, OK to create a new lock.
                            self.__log('PID '+str(self.oldpid)+' in '+str(self.lockfile)+' running but does not match '+str(self.thisExec))
                            if self.delete():
                                return True
                            return False
                else:
                    #
                    #File exists, but pid not running, remove lock file.
                    self.__log('PID '+str(self.oldpid)+' in '+str(self.lockfile)+' not running')
                    if self.delete():
                        return True
                    return False
            except Exception as e:
                self.Errors.append(e)
                return False
        #
        # No lock file, return OK
        return True
    def murder(self):
        """
        Try to kill pid found in the lock file.
        """
        self.__log('murder(self), Killable is'+str(self.Killable))
        if not self.Killable:
            #
            # Not allowed to `kill` so just return True.
            return True
        try:
            #
            # TODO: need to do field testing of os.kill.
            os.kill(self.oldpid, 9)
            return True
        except Exception as e:
            self.Errors.append(e)
            return False
        return False
def main():
	"""
    TODO: accept lock file from command line, just for shits and giggles.
    """
	return 0

if __name__ == '__main__':
	main()
