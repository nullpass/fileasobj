#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  npnutils.py
#  


def nowL():
    """
    Return a nice timestamp, normally used when printing debug info.
    format meant to mimic the result of `date` command using en_US
    locale

    Accepts:
    None

    Returns:
    t - str. String of a timestamp of the current time.

    Outputs:
    None
    
    """
    t = str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))
    return t
    
def bark(a):
    """
    Print a string with a timestamp if `debugg` is True

    Accepts:
    a - str, required. String to print

    Returns:
    None

    Outputs:
    a - str, if `debugg` is True

    This is how we easily show or hide all debug output.
    """
    if debugg: print nowL()+" "+thisProc+" "+a
    return
    
    
    
def require_path(p):
    """
    Require a path (diretory or file) and halt execution if it's not
    present.

    Accepts:
    p - str. Path to directory or file.
    
    Returns:
    None
    
    Outputs:
    Debug output if debugg is True
    
    """
    #bark("require "+p)
    if not os.path.exists(p):
        bark("FATAL Required path \""+p+"\" not found.")
        sys.exit(10)
    return

def require_create_path(p):
    """
    Require a file or dir, create if missing, halt if can't create.
    
    Accepts:
    p - str. Path to directory or file.

    Returns:
    None

    Outputs:
    Debug output if debugg is True
    
    """
    #bark("requireCreate "+p)
    if not os.path.exists(p):
        bark("WARNING Required path \""+p+"\" not found, being created.")
        if p[-1] == "/":
            try:
                os.mkdir(p,0700)
            except:
                bark("FATAL Failed to create required dir \""+p+"\"")
                sys.exit(10)
        else:
            try:
                f = open(p,'w')
                f.close()
            except:
                bark("FATAL Failed to create required file \""+p+"\"")
                sys.exit(10)
    return


def logger(event,thisFile):
    """
    Lovingly write a given event as string to file by file name.
    
    Accepts:
    event - str, message to log
    thisFile - str, full path to the file to log to.
    
    Returns:
    BOOLEAN
    
    Outputs:
    none

    """
    if os.path.exists(thisFile):
        try:
            f = open(thisFile, 'a')
            f.write(event + '\n')
            f.close()
        except:
            return False
    else:
        return False
    return True
    
    
    
def file_is_old_enough(thisPath,thisFile,ageDiff):
    """
    Check that a given file was modified within the past 'ageDiff' 
    seconds, if so return True.
    
    This function will replace new_discards() and provide debug output 
    to match the current code in stop_spam_vux() and stop_spam_domains()
    The code in those two functions will be updated to instead use this
    function.

    Accepts:
    thisPath - string, /-terminated path to thisFile  
    thisFile - string, name of file to check (no path)
    ageDiff - int, number of seconds in the past to define an acceptable
                age difference.
    
    Returns:
    BOOLEAN
    
    Outputs:
    debug output
    
    Todo:
    Decide how to handle file-not-found error, currently execution stops
    which is acceptable.
    
    Example:
    if file_is_old_enough("/tmp/","foo.txt",300):
        echo "/tmp/foo.txt was modified in the past 5 minutes"
    """
    #
    #when the given inbox file was last changed.
    mtimeOfFile = int(os.path.getmtime(thisPath+thisFile))
    #
    #the current time as a integer
    currTime = int(time.time())
    #
    #the difference between last change date and now, as a int.
    timeDiff = currTime - mtimeOfFile
    #
    #list the current from_domains file and its time information.
    bark("file="+thisFile+" now="+str(currTime)+" mtime="+str(mtimeOfFile)+" diff="+str(timeDiff)+" threshold="+str(ageDiff))
    #
    #if file is new enough to be considered valid...
    if int(time.time()) - int(os.path.getmtime(thisPath+thisFile)) <= int(ageDiff):
        return True
    return False    