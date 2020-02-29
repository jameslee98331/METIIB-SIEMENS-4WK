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
