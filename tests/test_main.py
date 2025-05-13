from mini_git.main import *
'''Testing repo/main functionality'''



if __name__ == "__main__":
    new_repo = Repository("test_repo")
    file_path = new_repo.dir_path
    #Random tests below
    empty_test_file = os.path.join(file_path, "test_file_empty.txt")

    with open(empty_test_file, "w") as f:
        f.write("")

    try:
        #Incorrect file
        fail_test = Blob("test3.txt")
        fail_test.store()
    except Exception as e:
        print(e)


    try:
        #No file given
        fail_test2 = Blob()
    except Exception as e:
        print(e)

    try:
        #Empty
        empty_test_blob = Blob(empty_test_file)
        empty_test_blob.store()
    except Exception as e:
        print(e)
