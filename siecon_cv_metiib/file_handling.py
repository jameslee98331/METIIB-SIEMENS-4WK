import os


def dir_empty(dirName):
    """
    Args:
        dirName (str): file path to directory containing image

    Returns:
        bool: True for empty directory, False for img present

    Raises:
        Exception: if img directory does not exist
    """
    # TODO: the pythonic way would still be to just try read a file and if it fails then loop
    if os.path.exists(dirName) and os.path.isdir(dirName):
        if os.listdir(dirName):
            return False
        else:
            return True
    else:
        raise Exception("Given Directory don't exists")


def first_img(dirName):
    """
    Args:
        dirName (str): file path to directory containing image

    Returns:
        str: file path to the first item in the directory
    """

    filename = os.listdir(dirName)

    # Only reads the first file in the directory
    return dirName + filename[0]
