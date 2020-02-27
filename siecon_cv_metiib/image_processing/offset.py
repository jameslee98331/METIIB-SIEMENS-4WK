import numpy as np


def centroid(kp_coord: list) -> tuple:
    """
    Args:
        kp_coord (list): list of tuples of keypoint locations

    Returns:
        tuple: mean location of keypoints (row, col)
    """

    x = [kp_coord[i][0] for i in range(len(kp_coord))]
    y = [kp_coord[i][1] for i in range(len(kp_coord))]
    return np.mean(x), np.mean(y)

# TODO:
# def find_scale(img, start, finish):
#     pass
#
# def pixel_to_mm():
#     pass
