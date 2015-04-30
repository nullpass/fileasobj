#!/usr/bin/env python3
"""
Feel free to change TestFile path or name as needed but leave TestContains as it is.

Be sure fileasobj is in your Python path.
"""
import unittest
from fileasobj import FileAsObj

TestFile = '/tmp/test_fileasobj.txt'

TestContains = """#/etc/hosts
# This is a test hosts file
#
#1
127.0.0.1 localhost.localdomain localhost

10.0.0.1 web01 web01.example.com

172.19.18.17    freebird.example.com

#comment

    #spaced comment
    # la deed da


192.168.192.168 h0stname.example.tld    h0stname
10.10.10.10     hostname.example.tld    hostname

10.2.3.4    mail01 mail01.example.tld
10.2.9.4    webmail01 webmail01.example.tld
10.2.5.2    www01   www01.example.tld
#172.8.8.8    www01   www01.example.tld
#
Checking for __contains__ functionality 123
#

# A bunch of duplicate empty comment lines....
#
#
#
#
#
#
#
"""


class TestAll(unittest.TestCase):

    def test_001_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            FileAsObj('#./././\/\/\/\/\/\/```!File does not exist........')

    def test_002_simple(self):
        test_file = FileAsObj()
        test_file.filename = TestFile # Create object even if file does not exist
        self.assertIsInstance(test_file, FileAsObj)

    def test_003_save_no_changes(self):
        test_file = FileAsObj()
        test_file.filename = TestFile # Create object even if file does not exist
        self.assertTrue(test_file.save())

    def test_004_save_with_changes(self):
        test_file = FileAsObj()
        test_file.filename = TestFile # Create object even if file does not exist
        test_file.contents = TestContains.split('\n') # Override file contents.
        self.assertEqual(TestContains, str(test_file)) # Confirm strings match
        self.assertTrue(test_file.save())

    def test_iter(self):
        test_file = FileAsObj(TestFile, verbose=True)
        for this in test_file:
            self.assertIsNotNone(this)

    def test_birthday(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertIsNotNone(test_file.birthday)

    def test_contains(self):
        test_file = FileAsObj(TestFile, verbose=True)
        result = False
        if 'Checking for __contains__ functionality 123' in test_file:
            result = True
        self.assertTrue(result)

    def test_not_contains(self):
        test_file = FileAsObj(TestFile, verbose=True)
        result = False
        if 'a7s6d9f7a6sd9f76asf9a8d7s89d6f967adfsadf' in test_file:
            result = True
        self.assertFalse(result)

    def test_egrep_char_list(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('h[o0]stname'))

    def test_egrep_word(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('bird'))

    def test_bad_regex(self):
        test_file = FileAsObj(TestFile, verbose=True)
        try:
            test_file.egrep('*rd')
        except Exception as error:
            self.assertEqual('nothing to repeat', str(error))

    def test_good_regex(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('.*rd'))

    def test_egrep_char_range(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('[a-z]ird'))

    def test_egrep_word_list(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('(host|bird)'))

    def test_egrep_string_end(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('tld$'))

    def test_egrep_string_start(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.egrep('^10.*'))


    def test_add_with_unique(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file + 'using __add__ three times, force unique')
        self.assertFalse(test_file + 'using __add__ three times, force unique')
        self.assertFalse(test_file + 'using __add__ three times, force unique')

    def test_append_with_unique(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.append('using __add__ three times, force unique'))
        self.assertFalse(test_file.append('using __add__ three times, force unique'))
        self.assertFalse(test_file.append('using __add__ three times, force unique'))

    def test_append_not_unique(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.append('using __add__ three times, force unique', unique=False))
        self.assertTrue(test_file.append('using __add__ three times, force unique', unique=False))
        self.assertTrue(test_file.append('using __add__ three times, force unique', unique=False))

    def test_subtract(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file - '#comment')

    def test_subtract_fail(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertFalse(test_file - 'this string does not exist in file!')

    def test_remove_multi(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(test_file.rm(test_file.grep('#')))

    def test_replace_whole_line(self):
        test_file = FileAsObj(TestFile, verbose=True)
        old = '172.19.18.17    freebird.example.com'
        new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
        self.assertTrue(test_file.replace(old, new))

    def test_replace_regex(self):
        test_file = FileAsObj(TestFile, verbose=True)
        old = test_file.egrep('^[ ]+#.*')
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        self.assertFalse(test_file.egrep('^[ ]+#.*'))

    def test_replace_list(self):
        test_file = FileAsObj(TestFile, verbose=True)
        old = ['#', '# ', '#1']
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        for this in old:
            self.assertFalse(test_file.check(this))

    def test_count_comment_empty(self):
        test_file = FileAsObj(TestFile, verbose=True)
        foo = test_file.grep('#')
        self.assertEqual(len(foo), 18)

    def test_string(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(str(test_file))

    def test_string_log(self):
        test_file = FileAsObj(TestFile, verbose=True)
        self.assertTrue(str(test_file.log))


if __name__ == '__main__':
    unittest.main()
