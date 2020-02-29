import numpy as np
import cv2 as cv


def read_image(filepath: str) -> np.ndarray:
    """
    Args:
        filepath (str): file path to the image being read

    Returns:
        np.ndarray: array of the image with RGB values
    """

    return cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)
