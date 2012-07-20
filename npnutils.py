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
