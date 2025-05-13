import os
import shutil
import unittest

from mini_git import Tree
from mini_git import decode_sha_to_path
from mini_git import Repository

class TestTree(unittest.TestCase):
    
    def setUp(self):
        self.repo_dir = "test_repo_tree"
        if os.path.exists(self.repo_dir):
            #destroys the path
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
        shutil.rmtree(self.repo_dir)
    

    def test_tree_store_and_load(self):
        #Create tree and store + save obj id
        tree = Tree(self.repo_dir)
        object_id = tree.store()

        #Assert that it exists
        self.assertIsNotNone(object_id)
        self.assertTrue(os.path.exists(decode_sha_to_path(object_id)))
        
        #returns tree obj
        loaded_tree = Tree.load(object_id)

        #assert that the obj_id is the same, and that it's a tree
        self.assertEqual(loaded_tree.object_id, object_id)
        self.assertEqual(loaded_tree.path_type, "tree")

        #2 files, 1 subdirectory
        self.assertEqual(len(loaded_tree.children), 3)

        #check each child
        for entry in loaded_tree.children:
            #double check that each child is a tuple()
            self.assertEqual(len(entry), 3)
            #Check that the first is either blob or tree
            self.assertIn(entry[0], ("blob", "tree"))
            #Then make sure both the other tuples are stored as strs
            self.assertIsInstance(entry[1], str)
            self.assertIsInstance(entry[2], str)

if __name__ == "__main__":
    unittest.main()