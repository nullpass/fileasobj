"""
fileasobj/examples.py

"""

"""
Reading a file, first example
If you check the result of .read it will tell you if it worked.
"""
my_file = FileAsObj()
if my_file.read('./input.txt'):
    print('File was loaded')
else:
    print('File was NOT loaded, here are the errors')
    print(my_file.trace)



"""
Reading a file, second example
If you read the file when you instantiate you must check .Errors
"""
my_file = FileAsObj(os.path.join('home','bob','clients.txt'), verbose=True)
if my_file.Errors:
    print(my_file.trace)
    sys.exit(10)



# Find mail servers in a hosts file that have IPs starting with 172
my_file.egrep('^172.*mail[0-9]')

