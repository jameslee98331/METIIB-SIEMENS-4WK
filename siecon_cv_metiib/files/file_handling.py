import os


def dir_empty(dirName):
    if os.path.exists(dirName) and os.path.isdir(dirName):
        if os.listdir(dirName):
            return False
        else:
            return True
    else:
        raise Exception("Given Directory don't exists")

def first_img(dirName):
    filename = os.listdir(dirName)

    # Only reads the first file in the directory
    return dirName + filename[0]
