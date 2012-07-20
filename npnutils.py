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
    
    