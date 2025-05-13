from main import *
'''Testing repo/main functionality'''



if __name__ == "__main__":
    file_path = initialize_repository("test_repo")
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
