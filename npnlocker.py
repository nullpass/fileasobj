#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
"""
npnlocker.py - Provide easy lock file management as a class

"Dissatisfied with the shape of a perfect circle I've reinvented the wheel, again."

by: nullpass, 2012; based loosely on gekitsuu's Mutex()

2012.08.xx - Initial release
______________________
Logic:
    If lock file does not exist: OK, create

    If lock file exists but proc not running: OK, delete, create
        [Previous instance failed to remove its lock file before exiting]

    If PID running and process matches str(thisExec) and the lock file is older than int(maxage): OK, kill, delete, create
        [A previous instance is stuck, kill it and allow a new instance to run]
        
    If PID running but the name of the process does not match str(thisExec): OK, delete, create
        [Previous instance failed to remove its lock file and some other process spawned later with the same PID]*
        
    If lock file exists, PID running and the process matches str(thisExec): FAIL
        [Previous instance still running, not old enough to kill]
______________________
Examples:

# Try to create a lock file using default settings (see __init__)
#
from npnlocker import Locker
mylock = Locker()
if mylock.create():
    ...
    ...code that requires a lock file here...
    ...
    mylock.delete()


# Try to create a lock file using a custom pid file. 
# Don't allow a previous instance to be killed.
# Set maximum age of the lock file to be 999999999 seconds.
#
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
______________________
Notes:

Be mindful of 'thisExec' even if you don't override it with a custom 
name.
The contents of /proc/'oldpid'/cmdline could be anything, and since the
logic only does a very simple substring check you might end up `kill`ing
a legitimate process that has a similar file name or argument. 
For example, if you named your 'thisExec' bob and there was another 
process that started later and happened to re-use the PID for a previous 
instance of `bob` and was named 'john.sh --path=/var/bob' then that 
process would get `kill`ed. 
The self.Killable variable gives you the chance to be careful with 
process management without sacrificing lock file functionality.

*You may think it is rather silly to worry about PID re-use, but I have 
to code on/for systems that stay online for years at a time, some have 
been up for over a decade, but whether or not it makes sense it is still
a valid error condition and one that is easy to check for. 
______________________
TODO:
    1. os.kill in Locker.murder() needs more testing
    2. Add basic funtionality to main() to allow locking with default 
        settings from the command line. Use sys.exit(0|1) to inform
        caller if locker was successful. --DONE, check main() for usage
"""
  
__version__ = '0.0.b'
import time
import os
from platform import node
import sys
import signal

class Locker:
    """
    Yu' sure gotta purddy lockfile.
    """
    def __init__(self):
        """
        Give birth, define default settings.
        """
        self.Birthday = (float(time.time()),str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())))
        #
        # Setting this to False will cause all methods to return True 
        # without actually doing anything.
        self.Enabled = True
        #
        # True = Let Locker.murder() os.kill an old pid found where the name of the process matches this application.
        # If False, Locker.murder() will return True but not actually os.kill
        self.Killable = True 
        #
        # List of any exceptions caught
        self.Errors = []
        #
        # String containing information about steps taken. Used for debugging
        """
        >>> print m.Trace
        Tue Aug 14 15:29:53 EDT 2012 python_3253[3253] check(self)
        Tue Aug 14 15:29:53 EDT 2012 python_3253[3253] PID file /home/me/m.pid found
        Tue Aug 14 15:29:53 EDT 2012 python_3253[3253] Get old PID from /home/me/m.pid
        Tue Aug 14 15:29:53 EDT 2012 python_3253[3253] PID 3212 in /home/me/m.pid not running
        Tue Aug 14 15:29:53 EDT 2012 python_3253[3253] delete(self)
        Tue Aug 14 15:30:02 EDT 2012 python_3253[3253] create(self)
        """
        self.Trace = ''
        #
        # Max age (in seconds) a lock file can be before it is 
        # considered invalid (too old to trust)
        self.maxage = int(1)     # 1 second
        self.maxage = int(300)   # 5 minutes
        self.maxage = int(3600)  # 1 hour
        self.maxage = int(43200) # 12 hours
        self.maxage = int(86400) # 24 hours
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
        #
        # If you need to double check lock status after calling Locker.create()
        self.Locked = False
    def __log(self,thisEvent):
        """
        Private method to update self.Trace with str(thisEvent) given
        as argument.
        """
        if not self.Enabled:
            return True
        self.Trace += str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+' '+self.thisHost+' '+self.thisProc+' '+str(thisEvent)+'\n'
        return
    def create(self):
        """
        check() for existing lock file, if that returns True create a 
        new lock file and return True.
        """
        if not self.Enabled:
            return True
        self.__log('create(self)')
        if self.check():
            try:
                fileHandle = open(self.lockfile, 'w')
                fileHandle.write(str(os.getpid()) + '\n')
                fileHandle.close()
                #
                # If we got this far everything worked, set Locked True
                self.Locked = True
                return True
            except Exception as e:
                self.Errors.append(e)
        return False
    def delete(self):
        """
        Remove the lock file. 
        This can also be accessed as mylock.remove()
        """
        if not self.Enabled:
            return True
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
        if not self.Enabled:
            return True
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
                    #
                    # PID is running, get name from /prod/oldpid/cmdline 
                    self.__log('PID '+str(self.oldpid)+' is running, check name in /proc/%s/cmdline')
                    if os.path.exists( '/proc/'+str(self.oldpid)+'/cmdline' ):
                        #
                        # Get string from 
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
                            else:
                                #
                                # Lock file was created recently, PID 
                                # still running and the process looks 
                                # like this application, refuse new lock
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
                    #else: #There is no /proc/oldpid/cmdline
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
        # No lock file, check() returns True, OK to create.
        self.__log('No lock file found')
        return True
    def murder(self):
        """
        Try to kill pid found in the lock file.
        """
        if not self.Enabled:
            return True
        self.__log('murder(self), Killable is: '+str(self.Killable))
        if not self.Killable:
            #
            # Not allowed to `kill` so just return True.
            return True
        try:
            #
            # send `kill -9 ${PID}`
            os.kill(int(self.oldpid), 9)
            return True
        except Exception as e:
            self.Errors.append(e)
        return False
def main():
    """
    If you want to use this for shell scripts or unix apps do this:
    
    me@pybox01:~$ python ./npnlocker.py create ./foo.pid ; echo $?
    0
    me@pybox01:~$ python ./npnlocker.py delete ./foo.pid ; echo $?
    0
    me@pybox01:~$ 
    
    in shell code
    python ./npnlocker.py create ./foo.pid || exit $?
    
    """
    if not sys.argv[1:] and sys.stdin.isatty(): sys.exit(1)
    mylock = Locker()
    if sys.argv[2:]:
        mylock.lockfile = sys.argv[2]
    #
    if 'create' in sys.argv[1]:
        if mylock.create():
            sys.exit(0)
        sys.exit(1)
    #
    if 'delete' in sys.argv[1]:
        if mylock.delete():
            sys.exit(0)
        sys.exit(1)
                    
    sys.exit(1)

if __name__ == '__main__':
    main()
