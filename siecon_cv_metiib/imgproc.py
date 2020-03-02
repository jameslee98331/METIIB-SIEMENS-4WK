import cv2 as cv
import numpy as np
from collections import namedtuple


def crop(img: np.ndarray, corner: namedtuple) -> np.ndarray:
    """
    Args:
        img (np.ndarray): array of the image with RGB values to be cropped
        corner (namedtuple): named tuple in the format namedtuple('rect', 'start, finish')
                             rect.start represents the top left corner of a cropping frame
                             rect.finish represents the bottom right corner of a cropping frame

    Returns:
        np.ndarray: array of the image with RGB values cropped with limits from corner (namedtuple)
    """

    return img[corner.start[0]:corner.finish[0], corner.start[1]:corner.finish[1]]


def mask(img: np.ndarray, corner: namedtuple) -> np.ndarray:
    """
    Args:
        img (np.ndarray): array of the image with RGB values to be masked
        corner (namedtuple): named tuple in the format namedtuple('rect', 'start, finish')
                             rect.start represents the top left corner of a masking frame
                             rect.finish represents the bottom right corner of a masking frame

    Returns:
        np.ndarray: array of a single channel mask with values 255 in ROI and 0 elsewhere
    """

    zeros = np.zeros(img.shape[:2], dtype=np.uint8)

    # draw your selected ROI on the mask image
    return cv.rectangle(zeros, corner.start, corner.finish, 255, thickness=-1)

# TODO: Manipulate contrast of the input image
# def contrast():
#     pass

def keypts(img: np.ndarray, mask: np.ndarray) -> tuple:
    """
    Args:
        img (np.ndarray): array of img for key point detection
        mask (np.ndarray): array of mask for ROI

    Returns:
        tuple:
            - list of tuples (row[i], col[i]) of keypoint locations
            - list of keypoint objects
    """

    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img, mask)

    # convert keypoint object to locations array
    return cv.KeyPoint_convert(kp), kp


def keypts_img(img: np.ndarray, key_points: cv.KeyPoint) -> np.ndarray:
    """
    Args:
        img (np.ndarray): array of img for key point detection
        key_points (cv.KeyPoint): list of keypoint objects

    Returns:
        img (np.ndarray): img input image overlaid with keypoints in green
    """

    # draw only keypoints location,not size and orientation
    return cv.drawKeypoints(img, key_points, img, color=(0, 255, 0), flags=0)


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




def extract_feature_centroid():



    pass
