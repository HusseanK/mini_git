import os


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
    

    def add(self, path: str):
        pass

    def commit(self, author: str, msg: str = None):
        pass
    
    def log(self, n=None):
        pass
    
    def read_commit(self, sha):
        pass

if __name__ == "__main__":
    new_repo = Repository("test_repo")