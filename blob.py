import hashlib
import os


from utils import *

'''
Blob hashing system
'''

class Blob:
    #Creates a blob class, taking in a file
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        if self.file_path is None:
            raise ValueError("Must provide a path to a file")
        
        self.object_id = None
        self.data = None
        
    #Used to store new blobs
    def store(self) -> str:
        '''
        Store a file as a blob

        Returns
        --------
        Blob object_id (*str*)
        '''
        #Validates the file
        validate_file(self.file_path)

        #Reads the data and sets it to the blob-object
        self.data = self._read_data(self.file_path)

        self.header = make_header("blob", self.data)
        
        self.object_id = create_obj_id(self.header, self.data)

        #Creating the folder and filename for use later
        self.folder, self.file_name = self.object_id[:2], self.object_id[2:]

        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

        write_to_disk(BASE_DIR, self.object_id, self.header + self.data)

        #returns the object_id, for access
        return self.object_id

    def _read_data(self, file_path: str) -> bytes:
        #Reads the file and returns it as bytes
        with open(file_path, "rb") as f:
            data = f.read()
        return data



    @classmethod
    def load(cls, object_id: str) -> "Blob":
        #Decode to path
        path = decode_sha_to_path(object_id)

        #Validate path exists
        validate_file(path)

        #Reads the given path
        with open(path, "rb") as open_blob:
            content = open_blob.read()

        #locates the first break point char that was saved in the header
        index = content.find(b'\0')
        #Decoding into a raw-header to preserve byte-form
        raw_header = content[:index+1]
        header, character_length = raw_header[:-1].decode().split()
        assert header == "blob", f"Expected blob, got {header}"

        #simple match-case to determine where to go, will update later
        body = content[index+1:index+int(character_length)+1]

        assert int(character_length) == len(body), f"Body is not {character_length} long, failure"

        new = cls.__new__(cls)
        new.data = body
        new.header = header
        new.object_id = object_id
        new.path = path
        new.folder, new.file_name = new.object_id[:2], new.object_id[2:]

        return new



    def __str__(self):
        return f"{self.file_name},{self.path}"

    def __repr__(self):
        return f"{self.file_name},{self.path}"