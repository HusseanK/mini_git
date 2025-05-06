'''
File and Directory validation for my mini-git

Contains:
    - make_header(), create_obj_id(), write_to_disk()
    - validate_file(), validate_directory()
'''
import os
import hashlib


def make_header(tag: str, body: bytes) -> bytes:
    '''
    Creates the header and returns as bytes

    Args:
        tag(str): Obj type (blob/tree)
        body(bytes): the data of what's being hashed
    
    Returns:
        a header b"tag " + str(len(body)) + b"\\0"
    '''
    return tag.encode("ascii") + b" " + str(len(body)).encode("ascii") + b"\0"

def create_obj_id(header: bytes, body: bytes) -> str:
    '''
    Creates the object id/Sha by joining header + body

    Args:
        header(bytes): the header
        body(bytes): the data of what's being hashed
    
    Returns:
        Object ID (str)
    '''
    return hashlib.sha256(header + body).hexdigest()

def write_to_disk(BASE_DIR: str, obj_id: str, obj_bytes: bytes) -> None:
    '''
    Writes the incoming data to a file

    Args:
        BASE_DIR(str): the base directory
        obj_id(str): the sha256 as a string
        ob_bytes(bytes): the object bytes as bytes (header+data)
    '''
    folder, file_name = obj_id[:2], obj_id[2:]
    folder_path = os.path.join(BASE_DIR, ".minigit","objects", folder)
    os.makedirs(folder_path, exist_ok=True)
    #full-link to directory
    new_file = os.path.join(folder_path, file_name)
    if not os.path.exists(new_file):
        #then creates the file and writes both the header and data
        with open(new_file, "wb") as out:
            #Writes with the header, to ensure it's being read as a "blob" 
            out.write(obj_bytes)



def validate_file(file_path: str) -> None:
    '''
    Validates a file and raises appropriate exceptions

    Args:
        file_path: The file path that is input
    
    Raises:
        FileNotFoundError:
            - if the file does not exist
        ValueError:
            - if the path is not a file
            - if the file is empty
        IOError: 
            - if the file cannot be read
    '''

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")
    try:
        with open(file_path, "rb") as f:
            if not f.read(1):
                raise ValueError(f"File is empty, Path: {file_path}")
    except OSError as e:
        raise IOError(f"File cannot be read, Path = {file_path} \n Exception = {e}") from e

def validate_directory(file_path: str) -> None:
    '''
    Checks if the path exists, and that it is a Folder / Directory

    Args:
        file_path: The file path that is input
    
    Raises:
        FileNotFoundError:
            - if the directory does not exist
        NotADirectoryError:
            - if the path isn't a directory
    '''
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No path to directory exists: {file_path}")

    if not os.path.isdir(file_path):
        raise NotADirectoryError(f"Path is not a directory: {file_path}")