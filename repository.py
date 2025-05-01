import os

def initialize_repository(file_path: str):
    #Ensure the filepath exists, otherwise creates it
    os.makedirs(file_path, exist_ok=True)

    minigit_path = os.path.join(file_path, ".minigit")
    objects = os.path.join(minigit_path, "objects")
    #ensures the new objects file_path exists
    os.makedirs(objects, exist_ok=True)
    #sets the base_dir for the new repo, to catch later
    os.environ["BASE_DIR"] = file_path
    return file_path

if __name__ == "__main__":
    initialize_repository("test_repo")
