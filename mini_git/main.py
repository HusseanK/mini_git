import os

from mini_git.repository import Repository
from mini_git.blob import Blob
from mini_git.tree import Tree



if __name__ == "__main__":
    new_repo = Repository("test_repo")
    file_path = new_repo.dir_path
    test_file = os.path.join(file_path, "test_file.txt")

    with open(test_file, "w") as f:
        f.write("hello, this is a test file")

    # #Creates the blob obj
    # test_blob = Blob(test_file)
    # #Stores it, and saves it's as the sha256
    # new_test = test_blob.store()
    # #Loads a blob using a SHa256
    # loaded_blob = Blob.load(new_test)
    # #Finds the path to a file using the sha256
    # blob_path = Blob.decode_blob_to_path(new_test)

    new_tree = Tree("test_repo")
    new_tree.store()