import unittest
import os
from random import randrange

from blob import Blob

#Unittesting for my blob-class
class TestBlob(unittest.TestCase):
    os.environ["BASE_DIR"] = "test_blobs"
    #just setting a random num str at the end of a test document, to add randomness
    random_num = str(randrange(0, 300))
    #uses the hook method setUp to create a new test.txt file
    def setUp(self):
        self.test_file = "test.txt"
        with open(self.test_file, "w") as f:
            f.write("This is just a test document" + self.random_num)

    #removes it after setting it up
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    #then tests the blob system
    def test_blob(self):
        #create and store blob
        blob = Blob(self.test_file)
        blob_path = blob.store()

        #load, currently returns the SHA of the object
        load_blob = Blob.load(blob_path)

        #assertion for unnittest, reads the SHA
        self.assertEqual(load_blob.data.decode(),("This is just a test document" + self.random_num))

#Run baby run
if __name__ == "__main__":
    unittest.main()