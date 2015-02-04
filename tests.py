"""

"""
import re
from fileasobj import FileAsObj

try:
    impossible = FileAsObj('File does not exist')
except FileNotFoundError as msg:
    print(msg)


test_file = FileAsObj('Test.txt', verbose=True)

#
# test iterable
for this in test_file:
    print(this)


print(test_file.birthday)


# test_file = FileAsObj('Test.txt')
# print(test_file)
# print(test_file.trace)

if 'Checking for __contains__ functionality 123' in test_file:
    print('__contains__ test string present')

if 'a7s6d9f7a6sd9f76asf9a8d7s89d6f967adfsadf' not in test_file:
    print('bogus string not in test file, good!')

test_file + 'using __add__ three times, force unique'
test_file + 'using __add__ three times, force unique'
test_file + 'using __add__ three times, force unique'
test_file.append('using append three times with unique')
test_file.append('using append three times with unique')
test_file.append('using append three times with unique')
test_file.append('using append three times without unique', unique=False)
test_file.append('using append three times without unique', unique=False)
test_file.append('using append three times without unique', unique=False)


x = '#comment'
print('subtract {0}'.format(x))
print(test_file - x)
print('---')


x = 'w.*rd'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

x = 'bird'
print('Find {0}'.format(x))
print(test_file.egrep(x))
print('---')

try:
    # Just using * is invalid,
    x = '*rd'
    print('Find {0}'.format(x))
    print(test_file.egrep(x))
except Exception as msg:
    print(type(msg))
    print(msg)

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
print('Remove {0} from {1}, RESULT={2}'.format(x, test_file.egrep(x), test_file.rm(test_file.egrep(x))))
print('---')

x = ' h0st.*'
print('Remove {0} from {1}, RESULT={2}'.format(
    x,
    test_file.egrep(x),
    test_file.rm(test_file.egrep(x)))
)
print('---')

x = '#'
print('Remove whole line "{0}" from {1}, RESULT={2}'.format(
    x,
    test_file.grep(x),
    test_file.rm(x))
)
print(test_file.grep(x))
print('---')

old = '172.19.18.17    freebird.example.com'
new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
print('Replace {0} with {1}'.format(old, new))
print(test_file.replace(old, new))
print('---')

x = '^[ ]+#.*'
print('Remove {0} from {1}, RESULT={2}'.format(
    x,
    test_file.egrep(x),
    test_file.rm(test_file.egrep(x)))
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

x = ['#', '# ', '#1']
y = '###'
print('replace {0} with {1}'.format(x, y))
print(test_file.replace(x, y))

print('Remove all lines that contain "#"')
test_file.rm(test_file.grep('#'))


print(test_file)
print(test_file.log)

