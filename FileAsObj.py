class FileAsObj:
    """
    Manage a file as an object. Each line of a file is added to the list
    'self.contents'. Lines that start with a # are ignored. Lines that
    already exist in the .contents lists are ignored- this uniqs the 
    data, however no sorting is done.
    Elements can be added or removed with .add and .rm. 
    The object's contents can be written back to the file, overwritting
    the file, with .write. 
    
    """
    def __init__(self,file):
        """
        read file into list varaible, uniq and without line breaks
        Ignore lines that start with #
        """
        self.contents = []
        bark("Read-only opening "+file)
        for line in fileinput.input(file):
            if line[0] is not "#":
                #
                #uniq the contents of the file when reading.
                line = line.strip("\n")
                if len(line) > 1 and line not in self.contents:
                    self.contents.append(line)
        fileinput.close()
        #
        #declare current state is original data from file.
        self.virgin = True
        #
        #set filename inside object, used during .write()
        self.filename = file
    def isVirgin(self):
        """
        self.virgin is True or False.
        True = hasn't changed since __init__
        False = something was added or removed from object.
        """
        return self.virgin
    def check(self,needle):
        """
        check existing contents of file for a string
        """
        if needle in self.contents:
            return True
        return False
    def add(self,item):
        """
        add item to end of list unless it already exists.

        """
        #
        #Check for the item.
        if item not in self.contents:
            #
            # not present, adding.
            self.contents.append(item)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # Already present, no changes made.
        return False
    def rm(self,item):
        """
        remove item from contents.
        """
        #
        #Check for item
        bark("Call to remove '"+item+"' from "+self.filename)
        if item in self.contents:
            #
            #item found, removed.
            self.contents.remove(item)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # wasn't there, nothing changed.
        return False
    def inventory(self):
        """
        return contents of self.contents
        
        Useful for printing contents, but hilariously redundant.
        """
        return self.contents
    def write(self):
        """
        write self.contents to self.filename
        self.filename was defined during __init__
        """
        bark("Writing "+self.filename)
        f = open(self.filename, "w")
        for line in self.contents:
            f.write(line+"\n")
        f.close()
        return True
