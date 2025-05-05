import os
import hashlib
from blob import Blob

class Tree:
    all_trees = []
    all_files = []
    BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

    def __init__(self, tree_path):
        self.tree_path = tree_path
        self.store()

    @classmethod
    def validate_self(cls, path):
        #just validate that the file is a dr
        if not path:
            raise FileNotFoundError("Error somewhere")
        #need logic to create blob if it's a file

        if os.path.isfile(path):
            new_blob = Blob(path)
            final = new_blob.store()
            Tree.all_files.append(final)
            return False
        #currently recursively creating a tree for everything inside a dir
        if os.path.exists(path):
            files = [Tree(os.path.join(cls.BASE_DIR,path, f)) for f in os.listdir(path)]
            Tree.all_trees.append(path)
            return True

        #Raising a base typeerror for now
        raise TypeError("File not found: ", path)


    def store(self):
        #Validation, if folder, hash
        Tree.validate_self(self.tree_path)
        #Need to hash dirname
        self.hash_file(self.tree_path)
        return
    
    def hash_file(self, path):
        new_str = path.encode()
        object_id = hashlib.sha256(new_str).hexdigest()
        return object_id


    def load(self, tree_path):
        return print(f"{tree_path}")
    
    def __str__(self):
        return str(self.tree_path)

if __name__ == "__main__":
    tree_path = os.path.join(f"..\\mini_git\\test_repo")
    new_tree = Tree(tree_path)

    print("Trees: ")
    for x in Tree.all_trees:
        print(x)
    
    print("Files: ")

    for f in Tree.all_files:
        print(f)