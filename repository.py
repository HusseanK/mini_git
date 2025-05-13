import os

def initialize_repository(dir_path: str):
    '''
    Takes in a dirpath and creates a new directory

    :raises:
        ValueError: If path is a file
    '''
    if os.path.isfile(dir_path):
        raise ValueError(f"Path is a file, not a directory: {dir_path}")
    #Ensure the filepath exists, otherwise creates it
    os.makedirs(dir_path, exist_ok=True)

    minigit_path = os.path.join(dir_path, ".minigit")
    objects = os.path.join(minigit_path, "objects")
    
    #Create head and reference sections to link commits
    create_head_and_ref(minigit_path)

    #ensures the new objects file_path exists
    os.makedirs(objects, exist_ok=True)
    #sets the base_dir for the new repo, to catch later
    os.environ["BASE_DIR"] = dir_path
    return dir_path

def create_head_and_ref(minigit_path):
    '''
    Takes in an existing minigit path and creates a new ref+header folder, as well as a head that points to it
    '''
    #Just creates the path at .minigit/refs/heads/
    os.makedirs(os.path.join(minigit_path, "refs", "heads"), exist_ok=True)
    #Creates a new file with the text pointing to the master (made on first commit)
    with open(os.path.join(minigit_path, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master")

if __name__ == "__main__":
    initialize_repository("test_repo")