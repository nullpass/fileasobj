#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
fileasobj.py - Manage a local file as an object. Store contents in a 
                uniq list and ignore commented lines.

nullpass, 2012

2012.08.15 - Full conversion to portability, added .read()
2012.07.20 - Initial release


______________________
Example:

$ cat ./input.txt
valid entry
#ignore this entry
# another comment
  # will read()/write() this entry
site.ltd
foo.bar
# The next line will not be added
a
# But .lol will be added:
.lol

from fileasobj import FileAsObj
input_txt = FileAsObj()

if input_txt.read('./input.txt'):
    print input_txt.contents
    input_txt.add('foo')
    input_txt.add('bar')
    input_txt.write()
else:
    print input_txt.Trace
    print input_txt.Errors

# contents would then be: ['valid entry', '  # will read()/write() this entry', 'site.ltd', 'foo.bar', '.lol', 'foo', 'bar']

"""
__version__ = '1.0.0'

import sys
import os
import fileinput
from platform import node
import time

class FileAsObj:
    """
    Manage a file as an object. Each line of a file is added to the list
    'self.contents'. Lines that start with a # are ignored. Lines that
    already exist in the .contents lists are ignored- this uniqs the 
    data, however no sorting is done.
    Elements can be added or removed with .add and .rm. 
    The object's contents can be written back to the file, overwritting
    the file, with .write. 
    
    """
    def __init__(self):
        """
        read file into list varaible, uniq and without line breaks
        Ignore lines that start with #
        """
        self.Birthday = (float(time.time()),str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())))
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
        self.thisProc = self.thisExec.rstrip('.py')+'['+str(os.getpid())+']'
        #
        # List of any exceptions caught
        self.Errors = []
        #
        # String containing information about steps taken. Used for debugging
        self.Trace = ''
        #
        #
        self.contents = []
        self.filename = None
        #
        #declare current state is original data from thisFile.
        self.virgin = True
    def __log(self,thisEvent):
        """
        Private method to update self.Trace with str(thisEvent)
        """
        self.Trace += str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+' '+self.thisHost+' '+self.thisProc+' '+str(thisEvent)+'\n'
        return
    def read(self,thisFile):
        """
        
        Open thisFile and write its contents to self.contents.
        Will not add duplicate lines or lines that start with #
        
        WILL add a line if it starts with a space or tab but has a #
        later in the line.
        
        FileAsObj.read('./inputfile.txt')
        """
        self.filename = str.strip(thisFile)
        try:
            self.__log('Read-only opening '+str(self.filename))
            for line in fileinput.input(self.filename):
                if line[0] is not "#":
                    #
                    # uniq the contents of the thisFile when read()ing.
                    # Ignore lines that have few then 2 characters
                    line = line.strip("\n")
                    if len(line) > 1 and line not in self.contents:
                        self.contents.append(line)
            fileinput.close()
            self.__log('Wrote '+str( len(self.contents) )+' lines')
            return True
        except Exception as e:
            self.__log('ERROR during read(self,thisFile)')
            self.Errors.append(e)
            return False
    def check(self,needle):
        """
        check existing contents of file for a string
        
        if myfile.check('foo'):
            -or-
        if 'foo' in myfile.contents:
        """
        if needle in self.contents:
            return True
        return False
    def add(self,thisItem):
        """
        add thisItem to end of list unless it already exists.
        """
        #
        #Check for the item.
        if thisItem not in self.contents:
            #
            # not present, adding.
            self.contents.append(thisItem)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # Already present, no changes made.
        return False
    def rm(self,thisItem):
        """
        remove thisItem from contents.
        """
        self.__log('Call to remove "'+str(thisItem)+'" from '+str(self.filename))
        #
        #Check for item
        if thisItem in self.contents:
            #
            #thisItem found, removed.
            self.contents.remove(thisItem)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # wasn't there, nothing changed.
        return False
    def inventory(self):
        """
        return contents of self.contents
        
        Useful for printing contents, but hilariously redundant.
        """
        return self.contents
    def write(self):
        """
        write self.contents to self.filename
        self.filename was defined during .read()
        
        There is no self.virgin check because we need to let the caller
        decide whether or not to write. This is useful if you want to 
        force an overwrite of a file that might have been changed on 
        disk even if self.contents did not change.
        
        You can do something like:
        if not stats.virgin:
            #
            #something changed, re-write the file.
            stats.write()

        """
        try:
            self.__log('Writing '+str(self.filename))
            fileHandle = open(self.filename, 'w')
            for thisLine in self.contents:
                fileHandle.write(thisLine+'\n')
            fileHandle.close()
            return True
        except Excetion as e:
            self.__log('ERROR in write(self)')
            self.Errors.append(e)
            return False
