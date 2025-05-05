'''
File and Directory validation for my mini-git

Contains:
    - validate_file()
    - validate_directory()
'''
import os

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