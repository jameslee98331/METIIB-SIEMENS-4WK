def img_exists(file_path):
    """
    Args:
        file_path (str): file path to image

    Returns:
        bool: True for empty or non-existent directory, False for img present
    """

    try:
        f = open(file_path)
        f.close()
        return False

    except FileNotFoundError:
        return True
