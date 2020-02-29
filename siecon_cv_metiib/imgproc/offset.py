import numpy as np


# TODO: optimisation needed
def centroid(kp_coord: list) -> tuple:
    """
    Args:
        kp_coord (list): list of tuples of keypoint locations

    Returns:
        tuple: mean location of keypoints (row, col)
    """

    x = [coord[0] for coord in kp_coord]
    y = [coord[1] for coord in kp_coord]
    return np.mean(x), np.mean(y)

# TODO:
# def find_scale(img, start, finish):
#     pass
#
# def pixel_to_mm():
#     pass
