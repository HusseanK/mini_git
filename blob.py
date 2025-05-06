import hashlib
import os


from utils import validate_file, make_header, create_obj_id, write_to_disk

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

        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

        write_to_disk(BASE_DIR, self.object_id, self.header + self.data)

        #returns the object_id, for access
        return self.object_id

    def _read_data(self, file_path: "Blob.file_path") -> bytes:
        #Reads the file and returns it as bytes
        with open(file_path, "rb") as f:
            data = f.read()
        return data
    
    # def create_object_id(self) -> None:
    #     #uses a  header to encode and hash the file
    #     self.header = b"blob " + str(len(self.data)).encode("ascii") + b"\0"
    #     #uses hashlib to hash the file
    #     self.object_id = hashlib.sha256(self.header + self.data).hexdigest()
    #     #unpacking the folder and file name
    #     self.folder, self.file_name = self.object_id[0:2], self.object_id[2:]
    
    # def create_path_to_object(self):
    #     BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
    #     object_path = os.path.join(BASE_DIR, ".minigit","objects")
    #     os.makedirs(object_path, exist_ok=True)
    #     self.path = os.path.join(object_path,self.folder)
    
    # def create_new_path(self) -> str:
    #     '''
    #     returns self.object_id
    #     '''
    #     if os.path.isfile(os.path.join(self.path,self.file_name)):
    #         return self.object_id
        
    #     #creates a new file
    #     os.makedirs(self.path, exist_ok=True)

    #     #full-link to directory
    #     directory_name = os.path.join(self.path, self.file_name)

    #     #then creates the file and writes both the header and data
    #     with open(directory_name, "wb") as out:
    #         #Writes with the header, to ensure it's being read as a "blob" 
    #         out.write(self.header + self.data)

    #     return self.object_id


    @classmethod
    def load(cls, object_id: "Blob.object_id") -> "Blob":
        #Decode to path
        path = cls.decode_blob_to_path(object_id)

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

        #simple match-case to determine where to go, will update later
        result = content[index+1:index+int(character_length)+1]

        new = cls.__new__(cls)
        new.data = result
        new.header = header
        new.object_id = object_id
        new.path = path
        new.folder, new.file_name = new.object_id[:2], new.object_id[2:]

        return new

    @classmethod
    def decode_blob_to_path(cls, object_id: "Blob.object_id") -> "os.path":
        folder, file_name = object_id[0:2], object_id[2:]
        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
        object_path = os.path.join(BASE_DIR, ".minigit","objects")
        return os.path.join(object_path, folder, file_name)


    def __str__(self):
        return f"{self.file_name},{self.path}"

    def __repr__(self):
        return f"{self.file_name},{self.path}"