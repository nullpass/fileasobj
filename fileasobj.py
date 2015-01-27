#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fileasobj.py - Manage a local file as an object. Store contents in a unique list and ignore commented lines.
Written to handle files that contain only text data, good for when you cannot or will not use a proper SQL database.
    Not useful for config files.

    Written by a SysAdmin who needed to treat files like databases.

    nullpass, 2012
    https://github.com/nullpass/fileasobj

Methods:
    .grep    find first occurance of substring in file
    .egrep   regex-find first occurance of substring in file (Remember to use '.*', not just '*')
    .add     Add given line to end of file
    .rm      Remove a line from file, give entire matching line.
    .check   Return line if line is in file, else return False
    .read    Read file into self.contents as list
    .write   Save list to file overriding file on disk
    .replace Replace a whole line (old, new)

Examples:

    #
    # Reading a file, first example
    #
    # If you check the result of .read it will tell you if it worked.
    my_file = FileAsObj()
    if my_file.read('./input.txt'):
        print('File was loaded')
    else:
        print('File was NOT loaded, here are the errors')
        print(my_file.trace)

    #
    # Reading a file, second example
    #
    # If you read the file when you instantiate you must check .Errors
    my_file = FileAsObj(os.path.join('home','bob','clients.txt'), verbose=True)
    if my_file.Errors:
        print(my_file.trace)
        sys.exit(10)

    #
    # Find mail servers in a hosts file that have IPs starting with 172
    my_file.egrep('^172.*mail[0-9]')

Attributes you usually care about:
    self.trace  A string log of all methods run on object including any errors
    self.errors A list log of any errors captured
    Verbose     BOOLEAN, if true file is .read() verbatim, comments and
                    short lines are NOT ignored and duplicate lines
                    are preserved.
                    Please remember that .rm() and .replace() will work
                    on duplicate lines.

An ever-so-slightly-non-apocryphal non-minor version history:
    2015.01.27 - .replace() now accepts list for param 'old'.
    2014.12.02 - V4, search methods can now return lists and .rm works on lists
    2014.09.09 - V3, added .replace(), removed .dump() and .inventory()
    2014.08.14 - Finally added __str__
    2014.08.11 - Tab fixes and print changes to comply with py3.
    2014.06.20 - V2, added [e]grep, dump and verbose; some code correction
    2012.08.15 - Full conversion to portability, added .read()
    2012.07.20 - Initial release

Testing:
    I write in Python 3.4x and occationally do testing in 2.6 and 2.7. This module
    /should/ work with anything between 2.6 and 3.4+ but no promises.


TODO:
    5.x:
        Remove all exception catching and error log.
        Replace critical error log with raise.
        + .append
        + .save(), calls write
        + __add__ calls .append


"""
__version__ = '4.1.0'

import os
from platform import node
import time
import re
import sys
sys.dont_write_bytecode = True


class FileAsObj(object):
    """
    Manage a file as an object-
            -For when you just can't be bothered to use a real database.


    Each line of a file is added to the list 'self.contents'.
    By default lines that start with a # are ignored.
    By default data in self.contents is unique.
    Lines are sorted by whatever order they appear in the file.
    Elements can be added or removed with .add and .rm.
    The object's contents can be written back to the file, overwriting
    the file, with .write.

    Error handling: I will try not to sys.exit or throw an exception.
        Ideally all errors are logged to self.trace and self.errors.
        It is thus the duty of the calling code to check for self.errors
        and act however is needed.

        self.trace is a log of everything the instance of this class
        did. If there is an exception it is included.

        self.errors is a list() of exception objects.

    """

    def __init__(self, filename=None, verbose=False):
        """
        You may specify the file to read() during instantiation, but be
        sure to check for self.errors.

        verbose - BE CAREFUL! If you enable verbose all of the lines in
            your file will be added to self.contents. This includes
            comments and duplicate lines. If you rely on this classes'
            .grep() or .egrep() methods be sure you understand that
            comments can be returned as a valid result!

        """
        self.birthday = (
            float(time.time()),
            str(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))
            )
        #
        # Name of file this is running as
        arg0 = str(os.path.basename(sys.argv[0])).replace('.py', '')
        if len(arg0) < 3 or len(arg0) > 255:
            #
            # If arg zero is invalid, name me Python
            arg0 = 'Python'
        #
        # Current executable and PID, like myapp[12345]
        self.logname = '{0}[{1}]'.format(arg0, os.getpid())
        #
        # List of any exceptions caught
        self.errors = list()
        #
        # Multi-line string of all steps taken.
        self.trace = ''
        #
        # The list where contents of the file are stored
        self.contents = list()
        #
        # Accept filename during instantiation, default is None.
        self.filename = filename
        #
        # If you gave me a file to read when instantiated, then do so.
        if self.filename:
            self.read(self.filename, verbose)
        #
        # Declare current state is original data from self.filename.
        self.virgin = True

    def __str__(self):
        """
        There's been much debate as to whether this should
        return self.filename or self.contents as a string.
        My first use case needed str(contents) so that's
        what I'm publishing.
        """
        return '\n'.join(self.contents)

    def __log(self, this):
        """
        Private method to update self.trace with thisEvent
        """
        self.trace = '{OG}{Now} {Host} {Proc} {Event}\n'.format(
            OG=self.trace,
            Now=time.strftime('%a %b %d %H:%M:%S %Z %Y', time.localtime()),
            Host=node(),
            Proc=self.logname,
            Event=this,
        )
        return

    def read(self, given_file, verbose=False):
        """
        Read given_file to self.contents, ignoring comments and duplicate lines.
        WILL add a line if it starts with a space or tab but has a # later in
        the line.
        """
        self.filename = str.strip(given_file)
        try:
            self.__log('Read-only opening {0}'.format(self.filename))
            with open(self.filename, 'r') as handle:
                for line in handle:
                    line = line.rstrip('\r\n')
                    #
                    # blank lines that were just \n become None,
                    # so make sure this pass of line exists
                    if line:
                        if verbose:
                            #
                            # Some crazy person enabled verbose, just
                            # add whatever is in the file to
                            # self.contents.
                            # May whatever god you believe in
                            #   have mercy on your code.
                            self.contents.append(line)
                        elif line[0] is not '#':
                            # Line is not a comment
                            #
                            #
                            # unique the contents of given_file when reading
                            # Ignore lines that have fewer than 2 characters
                            if len(line) > 1 and line not in self.contents:
                                self.contents.append(line)
            self.__log('Read {0} lines'.format(len(self.contents)))
            return True
        except Exception as err:
            self.__log('ERROR during read(self, given_file) : {0}'.format(err))
            self.errors.append(err)
        return False

    def check(self, needle):
        """
        check existing contents of file for a string

        This searches each line as a whole, if you want to see if
        a substring is in a line, use .grep() or .egrep() methods.

        If found, return the needle; makes it easier for some code
        to delete more efficiently.
        """
        if needle in self.contents:
            return needle
        return False

    def add(self, line, unique=True):
        """
        add 'line' to end of contents.
        By default will not create a duplicate line.
        If unique is False will add regardless of contents.
        """
        self.__log('Call to add "{0}" to {1}; unique={2}'.format(line, self.filename, unique))
        if unique is False:
            self.contents.append(line)
            self.virgin = False
            return True
        if line not in self.contents:
            self.contents.append(line)
            self.virgin = False
            return True
        return False

    def rm(self, this):
        """
        Remove all occurrences of 'this' from contents
            where 'this' is an entire line.

        If 'this' is a list object then remove all lines
        that wholly match each element of 'this'
        """
        self.__log('Call to remove "{0}" from {1}'.format(this, self.filename))
        if isinstance(this, str):
            this = this.split('\n')
        if not isinstance(this, list):
            # This usually means .rm() was called with False which is OK;
            # log it but don't die.
            self.__log('Argument given to .rm() not a string or list, was {0}'.format(type(this)))
            return False
        for element in this:
            if element in self.contents:
                while element in self.contents:
                    self.__log('Removed {0} from line {1} of {2}'.format(element, self.contents.index(element), self.filename))
                    self.contents.remove(element)
                    self.virgin = False
            else:
                self.__log('"{0}" not found in {1}'.format(element, self.filename))
                return False
        return True

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
            self.__log('Writing {0}'.format(self.filename))
            with open(self.filename, 'w') as handle:
                for this_line in self.contents:
                    handle.write(this_line+'\n')
            return True
        except Exception as err:
            self.__log('ERROR in write(self) : {0}'.format(err))
            self.errors.append(err)
        return False

    def grep(self, needle):
        """
        Search for a string like `grep string file`
            No regex support here.

        If 1 match, return line as string.
        If multiple matches return lines as list of strings.
        If no matches return False
        """
        retval = list()
        for line in self.contents:
            if needle in line:
                retval.append(line)
        if retval:
            if len(retval) == 1:
                return str(retval[0])
            else:
                return retval
        # all-else
        return False

    def egrep(self, pattern):
        """
        REGEX search for pattern in file

        If 1 match, return line as string.
        If multiple matches return lines as list of strings.
        If no matches return False
        """
        try:
            pattern = re.compile(pattern)
        except Exception as err:
            self.__log('ERROR in egrep({0}) : {1}'.format(pattern, err))
            self.errors.append(err)
            return False
        retval = list()
        for line in self.contents:
            if pattern.search(line):
                retval.append(line)
        if retval:
            if len(retval) == 1:
                return str(retval[0])
            else:
                return retval
        # all-else
        return False

    def replace(self, old, new):
        """
        Replace all lines of file that match 'old' with 'new'

        Will replace duplicates if found.

        :param old: False, list of strings, or string.
        :param new: string
        """
        self.__log('Replace "{0}" with "{1}" in {2}'.format(old, new, self.filename))
        if old is False:
            return False
        if isinstance(old, str):
            old = old.split('\n')
        if not isinstance(old, list):
            raise ValueError('Argument "old" not a string, list or False, was {0}'.format(type(old)))
        for this in old:
            if not isinstance(this, str):
                raise ValueError('{0} is not a string'.format(this))
            while this in self.contents:
                index = self.contents.index(this)
                self.virgin = False
                self.contents.remove(this)
                self.contents.insert(index, new)
        return True
