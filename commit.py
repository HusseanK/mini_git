import os
import datetime

from utils import *
from tree import Tree


class Commit:

    def __init__(self, dir_path, author, commit_message = None):
        self.dir_path = dir_path
        self.author = author
        self.date_time = datetime.datetime.now().isoformat()
        #Mainly for test purposes, may change later
        if not commit_message:
            self.commit_message = input("Please enter a commit message: ")
        else:
            self.commit_message = commit_message
        #Fail if no path
        if not self.dir_path:
            raise ValueError("Must provide a directory")

    def create_data(self):
        if self.parent_sha:
            data = f"Tree:{self.tree_sha}\nParent:{self.parent_sha}\nDate:{self.date_time}\nAuthor:{self.author}\nMessage:{self.commit_message}"
        else:
            data = f"Tree:{self.tree_sha}\nDate:{self.date_time}\nAuthor:{self.author}\nMessage:{self.commit_message}"
        return data
    
    def get_parent_sha(self, BASE_DIR):

        head_path = os.path.join(BASE_DIR, ".minigit", "HEAD")

        with open(head_path, "rb") as f:
            line = f.read().decode().strip()
        
        location = line.split(None, 1)[1]
        self.parent_location = os.path.join(BASE_DIR, ".minigit", location)

        if os.path.exists(self.parent_location):
            with open(self.parent_location,"rb") as f:
                parent_sha = f.read().decode().strip()
        else:
            parent_sha = None

        return parent_sha

    def store(self):
        #Validate again
        validate_directory(self.dir_path)

        #Set Base Dir
        BASE_DIR = os.getenv("BASE_DIR", os.getcwd())

        #Create new tree for the dir, returning the SHA
        self.tree_sha = Tree(self.dir_path).store()

        #Grab the parent sha if it exists, from minigit/refs/heads/master
        self.parent_sha = self.get_parent_sha(BASE_DIR)

        #Set the data
        self.data = self.create_data()

        #Encode body
        self.body = self.data.encode("ascii")
        #Create header and object id
        self.header = make_header("commit", self.body)
        self.object_id = create_obj_id(self.header, self.body)

        write_to_disk(BASE_DIR, self.object_id, self.header + self.body)

        with open(self.parent_location, "w") as f:
            f.write(self.object_id)
        #Resetting
        self.parent_sha = None
        return self.object_id
    
    @classmethod
    def load(cls, object_id):
        path = decode_sha_to_path(object_id)

        validate_file(path)

        with open(path, "rb") as f:
            content = f.read()
        
        #Extract the header and body
        index = content.find(b'\0')
        raw_header = content[:index + 1]
        header_str = raw_header[:-1].decode()
        header_type, length = header_str.split()
        #Make sure it's a tree
        assert header_type == "commit", f"Expected commit, got {header_type}"
        
        #decode data
        body = content[index + 1:]

        assert int(length) == len(body), f"Body is not {length} long, failure"

        lines = body.decode("ascii").splitlines()

        entries = dict()
        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                entries[key.lower()] = val

        
        #make new commit
        commit = cls.__new__(cls)
        commit.object_id = object_id
        commit.tree_sha = entries["tree"]
        commit.parent_sha = entries.get("parent")
        commit.date_time = entries["date"]
        commit.author = entries["author"]
        commit.commit_message = entries["message"]
        

        return commit