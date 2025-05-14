import os


from mini_git.utils import *


from mini_git.tree import Tree
from mini_git.blob import Blob
from mini_git.commit import Commit


class Repository:
    '''
        Takes in a dirpath and creates a new repo

        :raises:
            ValueError: If path is a file
    '''
    def __init__(self, dir_path: str):
        
        if os.path.isfile(dir_path):
            raise ValueError(f"Path is a file, not a directory: {dir_path}")
        #Ensure the filepath exists, otherwise creates it
        os.makedirs(dir_path, exist_ok=True)

        #Creates the hidden .minitgit file and objects within it
        minigit_path = os.path.join(dir_path, ".minigit")

        objects = os.path.join(minigit_path, "objects")
        
        #Create head and reference sections to link commits
        self.create_head_and_ref(minigit_path)

        #ensures the new objects file_path exists
        os.makedirs(objects, exist_ok=True)
        #sets the base_dir for the new repo, to catch later
        os.environ["BASE_DIR"] = dir_path
        self.dir_path = dir_path

    def create_head_and_ref(self, minigit_path):
        '''
        Takes in an existing minigit path and creates a new ref+header folder, as well as a head that points to it
        '''
        #Just creates the path at .minigit/refs/heads/
        os.makedirs(os.path.join(minigit_path, "refs", "heads"), exist_ok=True)
        #Creates a new file with the text pointing to the master (made on first commit)
        with open(os.path.join(minigit_path, "HEAD"), "w") as f:
            f.write("ref: refs/heads/master")
    

    def add(self, path: str) -> str:
        '''
        Takes in a path, and adds it to the repo

        Returns:
            obj_id(str): returns the object id as a SHA string
        '''
        #Create full path
        full_path = os.path.join(self.dir_path, path)
        
        #Validate and create new tree/blob, storing and setting type
        if os.path.isdir(full_path):
            validate_directory(full_path)
            new_sha = Tree(full_path).store()
            obj_type = "tree"
        elif os.path.isfile(full_path):
            validate_file(full_path)
            new_sha = Blob(full_path).store()
            obj_type = "blob"
        else:
            #Raise error if path is invalid
            raise ValueError(f"Path is not a File or Dir: {full_path}")
        
        #Create the index and store the info
        new_ind = os.path.join(self.dir_path, ".minigit", "index")
        
        #Gets the parent dir
        parent_dir = os.path.dirname(new_ind)

        #Create the dir if it doesn't exist
        os.makedirs(parent_dir, exist_ok=True)

        with open(new_ind, "a") as f:
            f.write(f"{obj_type} {path} {new_sha}\n")
        
        return new_sha
        


    def commit(self, author: str, msg: str = None) -> list[tuple]:

        #Read the index of staged entries
        index_path = os.path.join(self.dir_path, ".minigit", "index")
        with open(index_path, "r") as f:
            data = f.read().splitlines()

        #breakdown each tuple in data
        result_line = [tuple(line.split(" ", 2)) for line in data]

        index_tree = Tree.from_index(self.dir_path, result_line)
        root_tree_sha = index_tree.store()

        c  = Commit(self.dir_path, author, msg)
        commit_sha = c.store(root_tree_sha)

        open(os.path.join(self.dir_path, ".minigit", "index"), "w").close()

        return commit_sha

    def log(self, n=None):
        pass
    
    def read_commit(self, sha):
        pass

if __name__ == "__main__":
    new_repo = Repository("test_repo")

    new_repo.add("folder_1")
    new_repo.add("file_1.txt")

    new_repo.commit("test", "test message")