import re
import fileasobj

test_file = fileasobj.FileAsObj('File does not exist')
print(test_file.trace)

#test_file = fileasobj.FileAsObj('Test.txt', verbose=True)
test_file = fileasobj.FileAsObj('Test.txt')
print(test_file.trace)

x = 'w.*rd'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = 'bird'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

# Just using * is invalid, 
x = '*rd'
print('Find {0}'.format(x))
print(test_file.egrep(x))
# There ya go
x = '.*rd'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = 'b.*rd'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = '[a-z]ird'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = '(host|bird)'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = 'h[o0]stname'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = '.*mail[0-9]'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = 'tld$'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = '^10.*'
print('Remove {0} from {1}, RESULT={2}'.format(
        x,
        test_file.egrep(x),
        test_file.rm(test_file.egrep(x))
        )
      )
print('---')

x = ' h0st.*'
print('Remove {0} from {1}, RESULT={2}'.format(
        x,
        test_file.egrep(x),
        test_file.rm(test_file.egrep(x))
        )
      )
print('---')

x = '#'
print('Remove whole line "{0}" from {1}, RESULT={2}'.format(
        x,
        test_file.grep(x),
        test_file.rm(x)
        )
      )
print(test_file.grep(x))
print('---')

old = '172.19.18.17    freebird.example.com'
new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
print('Replace {0} with {1}'.format(old, new))
print(test_file.replace(old, new))
print('---')

# Replace does not yet support lists as input
#old = test_file.egrep('^[ ]+#.*')
#new = '#'
#print('Replace {0} with {0}'.format(old, new))
#print(test_file.replace(old, new))
# so instead...
x = '^[ ]+#.*'
print('Remove {0} from {1}, RESULT={2}'.format(
        x,
        test_file.egrep(x),
        test_file.rm(test_file.egrep(x))
        )
      )
print('---')




x = '#FOO'
print('Add line {0}'.format(x))
print(test_file.add(x))


x = '#FOO'
print('Add line {0}'.format(x))
print(test_file.add(x))

x = '#FOO'
print('non-unique Add line {0}'.format(x))
print(test_file.add(x, unique=False))





#print(test_file)
#print(test_file.trace)


