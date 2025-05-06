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
    
    def store(self) -> None:
        '''
        Used to store tree objects
        '''
        self.children = []
        self.path_type = Tree.check_path_type(self.tree_path)

        #Sort the list of directories in the current directory
        sorted_dir = sorted(os.listdir(self.tree_path))

        #loop over all and add all children SHAs to self.children
        for each_child in sorted_dir:
            path_type = Tree.check_path_type(os.path.join(self.tree_path, each_child))
            if path_type == "tree":
                self.children.append(Tree.handle_tree(self.tree_path, each_child))
            elif path_type == "blob":
                self.children.append(Tree.handle_file(self.tree_path, each_child))

        #Reads the data and sets it to the blob-object
        self.data = self.read_child_data()
        
        self.header = make_header("tree", self.data)
        self.object_id = create_obj_id(self.header, self.data)

        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

        write_to_disk(BASE_DIR, self.object_id, self.header + self.data)


        #Returnst the object id
        return self.object_id

    @staticmethod
    def check_path_type(path):

        if os.path.isfile(path):
            validate_file(path)
            return "blob"
        if os.path.exists(path):
            validate_directory(path)
            return "tree"
        
        raise FileNotFoundError("Path does not exist: ", path)


    
    def read_child_data(self) -> bytes:
        '''
        Reads the data and encodes it as bytes
        '''

        '''
        The data of the tree is a join of all the child object ids
        which are stored in self.children
        these are encoded to ascii and then changed into byte form
        '''
        return b"".join(child_obj_id.encode("ascii") for child_obj_id in self.children)



    @staticmethod
    def handle_file(path, child):
        new_blob = Blob(os.path.join(path, child))
        blob = new_blob.store()
        return blob
    
    @staticmethod
    def handle_tree(path, child):
        #currently recursively creating a tree for everything inside a dir
        new_tree = Tree(os.path.join(path, child))
        tree = new_tree.store()
        return tree
        

    @classmethod
    def load(cls, tree: "Tree"):
        return print(f"{tree}: {tree.object_id} \n{tree.children}")
    
    def __str__(self):
        return str(self.tree_path)

if __name__ == "__main__":

    tree_path = os.path.join(f"..\\mini_git\\test_repo")
    new_tree = Tree(tree_path)
    new_tree.store()

    Tree.load(new_tree)