#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
    pathic.py - Build keys, a hat size and borders.
  
    by: nullpass, 2012

    Example:
    
$ ./pathic.py xxx
pathic - xxx

4 @ [1, 2]
h57GfUVnEe3pRoVq
8yw9Wqb4FsvchPz4
8tkLCmLm8Ze52djQ

"""
___version___="2.0.3"
import random
import time
import datetime
from sys import argv

def planter():
    """
    
    Create an integer for random.seed to use without using any random methods.
    
    %f 	Microsecond as a decimal number [0,999999], zero-padded on the left
    
    """

    Seed = int( time.time() ) * ( int( datetime.datetime.now().strftime("%f") ) + 29 )
    Seed = Seed - int( datetime.datetime.now().strftime("%f") ) + 229
    Seed = Seed + 1291
    Seed = Seed / ( int( str(Seed)[-1] ) + 2 )
    return Seed
    
def grow():
    """
    
    Build a key, return as string. 
    
    """
    #
    # Define friendly root string
    Root = "abcdefghijkmopqrstuvwxyzQWERTYUPLKJHGFDAZXCVN92345678"
    #
    # Convert root to a list by character
    Items = list(Root)
    #
    # Create a random number of times to shuffle the list
    random.seed(planter())
    Range = range(random.randint(37,83))
    for i in Range:
        #
        # Shuffle the list in place.
        random.shuffle(Items)
    #
    # Build a list until it's 16 chr long.
    random.seed(planter())
    Result = []
    while len(Result) < 16:
        #
        # You have a 33% chance of choosing a random char to append
        # at this point in this loop.
        if random.randint(1, 3) == 3:
            #
            # If lucky, append random character to list.
            Result.append(random.choice(Items))
    #
    # Create a random number of times to shuffle the list
    random.seed(planter())
    Range = range(random.randint(3,89))
    for i in Range:
        #
        # Shuffle the list in place.
        random.shuffle(Result)
    #
    # Convert list to string by character
    Result = ''.join(Result)
    return Result

def border():
    """
    
    Return a random border from a list of valid borders as str.     
    
    """
    Borders = [ [1,2] , [1,3] , [2,3] ]
    random.seed(planter())
    return str(random.choice(Borders))
    
def hat():
    """
    
    Return a randomly chosen hat size as str, must be even number.
    
    """
    random.seed(planter())
    R = random.randrange(2, 14, 2)
    return str(R)
    
def main():
    """
    """
    D = {}
    Base = ""
    D['border'] = border()
    D['hatSize'] = hat()
    D['key1'] = grow()
    D['key2'] = grow()
    D['key3'] = grow()
    if argv[1:]:
        Base = argv[1]
    if D:
        print "pathic - %s " % Base
        print ""
        print "%s @ %s" % ( D['hatSize'], D['border'] )
        print D['key1']
        print D['key2']
        print D['key3']
        print ""
    return 0

if __name__ == '__main__':
	main()

