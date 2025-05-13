import os
import hashlib


from blob import Blob
from utils import *

class Tree:
    '''
    Tree organizing system for the mini-git
    used to store and load files/projects

    Init
    ----
    :tree_path(str): Requires a path to a file or directory
    '''

    def __init__(self, tree_path: str):
        self.tree_path = tree_path
        if self.tree_path is None:
            raise ValueError("Must provide a path to a project")
    
    def store(self) -> str:
        '''
        Used to store tree objects
        '''
        self.children = []
        self.path_type = Tree.check_path_type(self.tree_path)

        #Sort the list of directories in the current directory
        sorted_dir = sorted(os.listdir(self.tree_path))

        #loop over all and add all children SHAs to self.children
        for each_child in sorted_dir:
            if each_child == ".minigit":
                continue
            file_path = os.path.join(self.tree_path, each_child)
            path_type = Tree.check_path_type(file_path)
            if path_type == "tree":
                self.children.append((path_type, each_child, Tree.handle_tree(file_path)))
            elif path_type == "blob":
                self.children.append((path_type, each_child, Tree.handle_file(file_path)))

        #Reads the data and sets it to the blob-object
        self.data = self.read_child_data()
        
        self.header = make_header("tree", self.data)
        self.object_id = create_obj_id(self.header, self.data)

        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

        write_to_disk(BASE_DIR, self.object_id, self.header + self.data)


        #Returnst the object id
        return self.object_id

    @staticmethod
    def check_path_type(path:str) -> str:
        '''
        Validates the incoming path and returns a str value either "blob" or "tree"

        :Raises: FileNotFoundError if path doesn't exist
        '''
        if os.path.isfile(path):
            validate_file(path)
            return "blob"
        if os.path.isdir(path):
            validate_directory(path)
            return "tree"
        
        raise FileNotFoundError("Path does not exist: ", path)


    
    def read_child_data(self) -> bytes:
        '''
        Reads the data and encodes it as bytes
        '''
        '''
        Each obj in self.children is a tuple of (entry_type, file_name, obj_id)
        It then gets added to lines and joined. to be returned as data
        '''
        lines = []
        for entry_type, file_name, obj_id in self.children:
            lines.append(f"{entry_type} {file_name} {obj_id}")
        return "\n".join(lines).encode("ascii")



    @staticmethod
    def handle_file(path: str) -> str:
        '''
        Takes in a path and creates a blob obj

        **returns**(str): object id (sha256)
        '''
        new_blob = Blob(path)
        blob = new_blob.store()
        return blob
    
    @staticmethod
    def handle_tree(path: str) -> str:
        '''
        Takes in a path and creates a tree obj

        **returns**(str): object id (sha256)
        '''
        new_tree = Tree(path)
        tree = new_tree.store()
        return tree
        

    @classmethod
    def load(cls, object_id: str) -> "Tree":
        #Loads the stored tree-path and reads raw bytes
        path = decode_sha_to_path(object_id)
        validate_file(path)
        with open(path, "rb") as f:
            content = f.read()
        
        #Extract the header and body
        index = content.find(b'\0')
        raw_header = content[:index + 1]
        header_str = raw_header[:-1].decode()
        header_type, length = header_str.split()
        #Make sure it's a tree
        assert header_type == "tree", f"Expected tree, got {header_type}"

        #decode data
        body = content[index + 1:]
        assert int(length) == len(body), f"Body is not {length} long, failure"


        lines = body.decode("ascii").splitlines()


        children = []
        for line in lines:
            entry_type, file_name, obj_id = line.strip().split()
            children.append((entry_type, file_name, obj_id))
        
        #make new tree:
        tree = cls.__new__(cls)
        tree.object_id = object_id
        tree.header = raw_header
        tree.data = body
        tree.children = children
        tree.tree_path = None
        tree.path_type = "tree"

        return tree
    
    def __str__(self):
        return self.tree_path if self.tree_path else f"Tree {self.object_id}"

if __name__ == "__main__":
    
    tree_path = os.path.join(f"..\\test_repo")
    new_tree = Tree(tree_path)
    tree = new_tree.store()

    Tree.load(tree)