import cv2 as cv
import numpy as np
from collections import namedtuple


def read_image(filepath: str) -> np.ndarray:
    return cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)


def crop(img: np.ndarray, corner: namedtuple) -> np.ndarray:
    return img[corner.start[0]:corner.finish[0], corner.start[1]:corner.finish[1]]


def mask(img: np.ndarray, corner: namedtuple) -> np.ndarray:
    zeros = np.zeros(img.shape[:2], dtype=np.uint8)
    # draw your selected ROI on the mask image
    return cv.rectangle(zeros, corner.start, corner.finish, 255, thickness=-1)

# TODO: Manipulate contrast of the input image
# def contrast():
#     pass
