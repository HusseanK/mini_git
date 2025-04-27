import hashlib
import os

'''
Blob hashing system
'''

class Blob:
    #Creates a blob class, taking in a file
    def __init__(self, file = None):
        self.file = file

    #Used to store new blobs
    def store(self):
        #sets the classes data for easier access later
        self.data = self.data_to_read()
        #Unpacks the 4 using the hash_file() func
        self.header, self.path, self.folder, self.file_name = self.hash_file()
        #Checks whether or not the file already exists, and then creates the folder if need be
        self.check_existing()
        #returns the file-name, for access
        return f'{self.path}/{self.file_name}'

    def data_to_read(self):
        #Reads the file and returns it, to allocate the self.data var
        with open(self.file, "rb") as f:
            data = f.read()
        return data
    
    def hash_file(self):
        #uses a  header to encode and hash the file
        header = b"blob " + str(len(self.data)).encode("ascii") + b"\0"
        #uses hashlib to hash the file
        sha1 = hashlib.sha1(header + self.data).hexdigest()
        #unpacking the folder and file name
        folder, file_name = sha1[0:2], sha1[2:]
        path = os.path.join("../mini_git/objects/",folder)
        #returns each, to set the self.var to the proper names
        return header, path, folder, file_name
        
    #Used to check whether a folder is already existing
    def check_existing(self):
        if os.path.isfile(self.path + "/" + self.file_name):
            print("File already exists")
            return self.file_name
        else:
            self.create_new_path()

    def create_new_path(self):
        #creates a new file
        os.makedirs(os.path.join(self.path), exist_ok=True)
        #then creates the file and writes both the header and data
        with open(os.path.join(self.path, self.file_name), "wb") as out:
            #Writes with the header, to ensure it's being read as a "blob" 
            out.write(self.header + self.data)

    
    @classmethod
    def load(cls, path):
        #Reads the given path
        with open(path, "rb") as open_blob:
            content = open_blob.read()

        #locates the first break point char that was saved in the header
        index = content.find(b'\0')
        #Everything before this, is the header + char length
        header, character_length = content[0:index].decode().split()
        #simple match-case to determine where to go, will update later
        result = content[index+1:index+int(character_length)+1]

        
        new = cls.__new__(cls)
        new.data = result
        new.header = header
        new.path = path
        new.folder = os.path.dirname(path)
        new.file_name = os.path.basename(path)
        return new


    def __str__(self):
        return f"{self.file_name},{self.path})"

    def __repr__(self):
        return f"{self.file_name},{self.path})"