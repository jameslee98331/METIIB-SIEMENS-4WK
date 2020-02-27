import cv2 as cv
import numpy as np


def keypts(img: np.ndarray, mask: np.ndarray) -> tuple:
    """
    Args:
        img (np.ndarray): array of img for key point detection
        mask (np.ndarray): array of mask for ROI

    Returns:
        tuple:
            - list of keypoint locations in tuples of (row[i], column[i])
            - list of keypoint objects
    """

    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    keypts = orb.detect(img, mask)

    # convert keypoint object to locations array
    return cv.KeyPoint_convert(keypts), keypts


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
