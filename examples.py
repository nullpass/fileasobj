"""
fileasobj/examples.py

"""
import sys
import os

from fileasobj import FileAsObj


# Reading a file
my_file = FileAsObj()
try:
    my_file.read('./input.txt')
except Exception as msg:
    print('File was NOT loaded, here are the errors')
    print(msg)


# Reading a file during instantiation and catching errors.
try:
    my_file = FileAsObj(os.path.join(os.sep, 'home', 'bob', 'clients.txt'), verbose=True)
except Exception as msg:
    print(msg)
    sys.exit(10)

#
# If your file does not yet exist...
new_file = FileAsObj()
new_file.filename = './new_file.txt'
new_file.add('new data')
new_file.save()  # This will create the file on disk and put your data into it.
#


#
# Find mail servers in a hosts file that have IPs starting with 172
my_file.egrep('^172.*mail[0-9]')


#
# Check for a line in file.
#    if 'This entire line' in my_file:
#        return True
#
# or simply:
#    return my_file.check('This entire line')
#
#

#
# Three methods to append a given line to the file, all work the same
my_file.add('foo')
my_file.append('foo')
print(my_file + 'foo')


#
# Add line even if it exists in the file already.
my_file.add('foo', unique=False)


#
# Print number of lines in the file (as it exists in memory)
print(len(my_file))


#
# Remove all lines that are "foo bar"
my_file.rm('foo bar')
# or
print(my_file - 'foo bar')


#
# Get all lines that contain a #
result = my_file.grep('#')


#
# Remove all lines that contain the word "foo"
# NOTE: this is dangerous and rarely needed.
my_file.rm(my_file.grep('foo'))


#
# Check for line in file, if exists remove it
if 'foo bar' in my_file:
    my_file.rm('foo bar')
# or
my_file.rm(my_file.check('foo bar'))
# or
my_file.rm('foo bar')  # OK if line not found.


#
# Now that you've changed data let's save it back to disk.
my_file.save()
# or
my_file.write()
# of
if my_file.virgin is False:
    my_file.save()


#
# NOTE: you'll probably never need to worry about this part. If it doesn't make sense, just ignore it.
# As things are checked or changed with FileAsObj an internal log is updated.
# To view it:
print(my_file.log)
# If you want to manually add something:
my_file.log('A manual log entry')  # This does not change the file, just the log attribute of the object.
