from repository import initialize_repository
from blob import Blob
import os


if __name__ == "__main__":
    file_path = initialize_repository("test_repo")
    test_file = os.path.join(file_path, "test_file.txt")

    with open(test_file, "w") as f:
        f.write("hello, this is a test file")

    #Creates the blob obj
    test_blob = Blob(test_file)
    #Stores it, and saves it's as the sha256
    new_test = test_blob.store()
    #Loads a blob using a SHa256
    loaded_blob = Blob.load(new_test)
    #Finds the path to a file using the sha256
    blob_path = Blob.decode_blob_to_path(new_test)