import numpy as np


def centroid(kp_coord: list):
    x = [kp_coord[i][0] for i in range(len(kp_coord))]
    y = [kp_coord[i][1] for i in range(len(kp_coord))]
    return np.mean(x), np.mean(y)


def y_centroid_rev(img, y_centroid):
    return (img.shape[1] - 1) - y_centroid[1]

# TODO:
# def find_scale(img, start, finish):
#     pass
#
# def pixel_to_mm():
#     pass
