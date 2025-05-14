import os
import shutil
import unittest

from mini_git import Commit
from mini_git import decode_sha_to_path
from mini_git import Repository

class TestCommit(unittest.TestCase):

    def setUp(self):
        #Set up creates the directory and adds a few test_files, to be deleted after
        self.repo_dir = "test_repo_commit"
        if os.path.exists(self.repo_dir):
            shutil.rmtree(self.repo_dir)
        
        os.makedirs(self.repo_dir)
        Repository(self.repo_dir)

        with open(os.path.join(self.repo_dir, "file1.txt"), "w") as f:
            f.write("this is file 1")
        
        with open(os.path.join(self.repo_dir, "file2.txt"), "w") as f:
            f.write("this is file 2")

        nested_dir = os.path.join(self.repo_dir, "nested")
        os.makedirs(nested_dir)

        with open(os.path.join(nested_dir, "nested_file.txt"), "w") as f:
            f.write("nested file")
        
    def tearDown(self):
        #Delete after done
        shutil.rmtree(self.repo_dir)
    

    def test_commit_store_and_load(self):
        #Create a commit, store and load it, with assertion tests
        commit = Commit(self.repo_dir, "test", commit_message = "this is a test")
        object_id = commit.store(commit)
        
        #Assert that it exists
        self.assertIsNotNone(object_id)
        self.assertTrue(os.path.exists(decode_sha_to_path(object_id)))

    
        loaded_commit = Commit.load(object_id)

        self.assertIsNotNone(loaded_commit.date_time)
        self.assertEqual(loaded_commit.commit_message, "this is a test")
        self.assertEqual(loaded_commit.author, "test")



if __name__ == "__main__":
    unittest.main()