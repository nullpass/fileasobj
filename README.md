fileasobj.py
======
Manage a local file as an object. Store contents in a unique list and ignore commented lines.
Written to handle files that contain only text data, good for when you cannot or will not use a proper SQL database.

* Not useful for config files.
* Written by a SysAdmin who needed to treat files like databases.


### An ever-so-slightly-non-apocryphal non-minor version history:
* 2014.12.02 - V4, search methods can now return lists and .rm works on lists
* 2014.09.09 - V3, added .replace(), removed .dump() and .inventory()
* 2014.08.14 - Finally added __str__
* 2014.08.11 - Tab fixes and print changes to comply with py3.
* 2014.06.20 - V2, added [e]grep, dump and verbose; some code correction
* 2012.08.15 - Full conversion to portability, added .read()
* 2012.07.20 - Initial release
