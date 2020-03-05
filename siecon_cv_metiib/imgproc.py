import cv2 as cv
import numpy as np
from collections import namedtuple


def draw_rect(start: tuple, finish: tuple) -> namedtuple:
    """
    Args:
        start (tuple): tuple of int of start location of rectangle
        finish (tuple): tuple of int of end location of rectangle

    Returns:
        namedtuple: ('start': (row, col), 'finish': (row, col))
    """

    rect = namedtuple('rect', 'start, finish')
    return rect(start, finish)


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


def draw_mask(img: np.ndarray, corner: namedtuple) -> np.ndarray:
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


def centroid(kp_coord: list) -> tuple:
    """
    Args:
        kp_coord (list): list of tuples of keypoint locations

    Returns:
        tuple: mean location of keypoints (row, col)
    """

    x = [coord[0] for coord in kp_coord]
    z = [coord[1] for coord in kp_coord]
    return np.mean(x), np.mean(z)


def extract_feature_centroid(img: np.ndarray, mask_rect: namedtuple) -> tuple:
    """
    Args:
        img (np.ndarray): preprocessed image for feature detection
        mask_rect: ROI for feature detection

    Returns:
        tuple: (centroid of feature keypoints in (x,y), key point objects)
    """

    mask = draw_mask(img, mask_rect)
    kp_coord, kp = keypts(img, mask)
    return centroid(kp_coord), kp


# TODO: This function needs some refactoring when in production environment
def calibration_rect(cropped_img: np.ndarray, X_RANGE_LEFT: tuple, X_RANGE_RIGHT: tuple,
                     Y_RANGE_TOP: tuple, Y_RANGE_BOT: tuple) -> tuple:
    """
    Args:
        cropped_img (ndarray): cropped image for calibration
        X_RANGE_LEFT (tuple): range of col indices for left vertical edge
        X_RANGE_RIGHT (tuple): range of col indices for right vertical edge
        Y_RANGE_TOP (tuple): range of row indices for top horizontal edge
        Y_RANGE_BOT (tuple): range of row indices for bottom horizontal edge

    Returns:
        tuple: (list of tuples of calibration coordinates in (x,y), key point objects)
    """

    # Extract feature of top left corner
    MASK_TOP_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_TOP[0])
    MASK_TOP_LEFT_FINISH = (X_RANGE_LEFT[1], Y_RANGE_TOP[1])
    mask_top_left_rect = draw_rect(MASK_TOP_LEFT_START, MASK_TOP_LEFT_FINISH)
    key_pts_top_left_centroid, key_pts_top_left = extract_feature_centroid(cropped_img, mask_top_left_rect)

    # Extract feature of top right corner
    MASK_TOP_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_TOP[0])
    MASK_TOP_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_TOP[1])
    mask_top_right_rect = draw_rect(MASK_TOP_RIGHT_START, MASK_TOP_RIGHT_END)
    key_pts_top_right_centroid, key_pts_top_right = extract_feature_centroid(cropped_img, mask_top_right_rect)

    # Extract feature of bottom left corner
    MASK_BOT_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_BOT[0])
    MASK_BOT_LEFT_END = (X_RANGE_LEFT[1], Y_RANGE_BOT[1])
    mask_bot_left_rect = draw_rect(MASK_BOT_LEFT_START, MASK_BOT_LEFT_END)
    key_pts_bot_left_centroid, key_pts_bot_left = extract_feature_centroid(cropped_img, mask_bot_left_rect)

    # Extract feature of bottom right corner
    MASK_BOT_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_BOT[0])
    MASK_BOT_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_BOT[1])
    mask_bot_right_rect = draw_rect(MASK_BOT_RIGHT_START, MASK_BOT_RIGHT_END)
    key_pts_bot_right_centroid, key_pts_bot_right = extract_feature_centroid(cropped_img, mask_bot_right_rect)

    loc = [key_pts_top_left_centroid, key_pts_top_right_centroid, key_pts_bot_left_centroid, key_pts_bot_right_centroid]
    kp = key_pts_top_left + key_pts_top_right + key_pts_bot_left + key_pts_bot_right

    return loc, kp


# TODO: This function needs some refactoring when in production environment
def find_scale(loc: list, col_const: float, row_const: float) -> np.ndarray:
    """
    Args:
        loc (list): list of 4 corner coordinates in tuples (x,y)
        col_const (float): length of horizontal feature in mm
        row_const (float): length of vertical feature in mm

    Returns:
        np.ndarray: scale factor converting from pixels to mm
    """

    # Calculate the length of the two edges in pixels
    top_edge = np.mean([(loc[1][0] - loc[0][0]), (loc[3][0] - loc[2][0])])
    vert_edge = np.mean([(loc[2][1] - loc[0][1]), (loc[3][1] - loc[1][1])])

    # Calculate the pixel per mm scale factor, top_edge = 33mm, vert_edge = 14mm
    return np.mean([top_edge / col_const, vert_edge / row_const], dtype=np.float64)
