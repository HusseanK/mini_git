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
        


    def commit(self, author: str, msg: str = None) -> str:
        '''
        Create a new commit from entries.

        Args:
            author: Name/Email
            msg: The commit message
        
        Raises:
            FileNotFoundError: If the staging index doesn't exist
            Runtime Error: If no entries are staged

        
        Returns:
            The Sha-256 object id of the new commit
        '''


        #Read the index of staged entries
        index_path = os.path.join(self.dir_path, ".minigit", "index")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Path does not exist: {index_path}, please run add() first")
        
        with open(index_path, "r") as f:
            data = f.read().splitlines()

        #Make sure something is actually ready to be committed
        if not data:
            raise RuntimeError("Nothing staged, run add() first")

        #breakdown each tuple in data (type, relative_path, sha)
        entries = [tuple(line.split(" ", 2)) for line in data]

        #Create new tree and then store
        index_tree = Tree.from_index(self.dir_path, entries)
        root_tree_sha = index_tree.store()

        commit_obj = Commit(self.dir_path, author, msg)
        commit_sha = commit_obj.store(root_tree_sha)

        #empty the index for the next commit
        open(index_path, "w").close()

        return commit_sha
    

    def log(self, n=None):
        '''
        Return upto the last n amount of commits. Otherwise return all.
        '''

        #Open the head to find the ref loc
        head_path = os.path.join(self.dir_path, ".minigit", "HEAD")
        with open(head_path, "r") as f:
            data = f.read().strip()

        #Grab the location and find latest commit
        last_commit_ref = data.split(None, 1)[1]
        ref_path = os.path.join(self.dir_path, ".minigit", last_commit_ref)
        #Open the sha
        with open(ref_path, "r") as f:
            current_sha = f.read().strip()

        full_list = []
        #loop through all the parent_sha's until N or None
        count = 0
        while current_sha and (n is None or count < n):
                commit = self.read_commit(current_sha)
                full_list.append(commit)
                current_sha = commit.parent_sha
                count += 1

        return full_list


    
    def read_commit(self, obj_id):
        '''
        Load a commit by the obj_id/sha and return commit instance.
            Also loads the tree and sets it under self.tree
        '''
        if not obj_id:
            raise ValueError(f"No id/sha provided")
        
        #Find path and validate existence
        path = decode_sha_to_path(obj_id)
        validate_file(path)
        
        #Load commit
        new_commit = Commit.load(obj_id)
        #Also load the tree it exists within
        new_commit.tree = Tree.load(new_commit.tree_sha)
        return new_commit
    


    def read_object(self, obj_id: str):
        '''
        Given an object_id return the corresponding Blob or Tree instance

        Args:
            obj_id (str): 40-char sha256 identifying the object
        '''
        if not obj_id or not isinstance(obj_id, str):
            raise ValueError(f'No id provided, or invalid type: {obj_id!r}')
        
        #validate path to ensure it exists
        path = decode_sha_to_path(obj_id)
        validate_file(path)


        #read the raw bytes and decode the header, setting obj type
        with open(path, "rb") as f:
            raw = f.read()
        index = raw.find(b'\0')
        if index < 0:
            raise ValueError(f"Corrupt object: {obj_id}")
        header_str = raw[:index].decode("ascii")
        object_type, _ = header_str.split(" ", 1)

        if object_type == "blob":
            return Blob.load(obj_id)
        elif object_type == "tree":
            return Tree.load(obj_id)
        else:
            raise ValueError(f"Unknown object type: {object_type} in {obj_id!r}")


if __name__ == "__main__":
    new_repo = Repository("test_repo")

    # test_folder = new_repo.add("folder_1")
    # test_file = new_repo.add("file_1.txt")

    # test_com = new_repo.commit("test", "test message")

    print(new_repo.log(3))