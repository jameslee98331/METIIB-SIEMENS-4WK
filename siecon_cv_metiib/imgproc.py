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
            - list of tuples (col[i], row[i]) of keypoint locations
            - list of keypoint objects
    """

    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img, mask)

    # convert keypoint object to locations array (column(x), row(y))
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
        tuple: mean location of keypoints (col, row)
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
        tuple:
            - centroid (col, row) of keypoint locations
            - list of keypoint objects
    """

    mask = draw_mask(img, mask_rect)
    kp_coord, kp = keypts(img, mask)
    return centroid(kp_coord), kp


# TODO: This function needs some refactoring when in production environment
def calibration_rect(cropped_img: np.ndarray, x_range_left: tuple, x_range_right: tuple,
                     y_range_top: tuple, y_range_bot: tuple) -> tuple:
    """
    Args:
        cropped_img (ndarray): cropped image for calibration
        x_range_left (tuple): range of col indices for left vertical edge
        x_range_right (tuple): range of col indices for right vertical edge
        y_range_top (tuple): range of row indices for top horizontal edge
        y_range_bot (tuple): range of row indices for bottom horizontal edge

    Returns:
        tuple:
            - namedtuple(top_left, top_right, bot_left, bot_right) of keypoint locations in (col[i], row[i])
            - list of keypoint objects
    """

    # Extract feature of top left corner
    mask_top_left_start = (x_range_left[0], y_range_top[0])
    mask_top_left_finish = (x_range_left[1], y_range_top[1])
    mask_top_left_rect = draw_rect(mask_top_left_start, mask_top_left_finish)
    key_pts_top_left_centroid, key_pts_top_left = extract_feature_centroid(cropped_img, mask_top_left_rect)

    # Extract feature of top right corner
    mask_top_right_start = (x_range_right[0], y_range_top[0])
    mask_top_right_end = (x_range_right[1], y_range_top[1])
    mask_top_right_rect = draw_rect(mask_top_right_start, mask_top_right_end)
    key_pts_top_right_centroid, key_pts_top_right = extract_feature_centroid(cropped_img, mask_top_right_rect)

    # Extract feature of bottom left corner
    mask_bot_left_start = (x_range_left[0], y_range_bot[0])
    mask_bot_left_end = (x_range_left[1], y_range_bot[1])
    mask_bot_left_rect = draw_rect(mask_bot_left_start, mask_bot_left_end)
    key_pts_bot_left_centroid, key_pts_bot_left = extract_feature_centroid(cropped_img, mask_bot_left_rect)

    # Extract feature of bottom right corner
    mask_bot_right_start = (x_range_right[0], y_range_bot[0])
    mask_bot_right_end = (x_range_right[1], y_range_bot[1])
    mask_bot_right_rect = draw_rect(mask_bot_right_start, mask_bot_right_end)
    key_pts_bot_right_centroid, key_pts_bot_right = extract_feature_centroid(cropped_img, mask_bot_right_rect)

    rect_corner_coords = namedtuple('rect_corner_coords', 'top_left, top_right, bot_left, bot_right')
    rect_corner_coords = rect_corner_coords(key_pts_top_left_centroid, key_pts_top_right_centroid, key_pts_bot_left_centroid, key_pts_bot_right_centroid)
    kp = key_pts_top_left + key_pts_top_right + key_pts_bot_left + key_pts_bot_right

    return rect_corner_coords, kp


# TODO: This function needs some refactoring when in production environment
def find_scale(rect_corner_coords: namedtuple, col_const: float, row_const: float) -> np.ndarray:
    """
    Args:
        rect_corner_coords (namedtuple): namedtuple of 4 corner coordinates in tuples (x,y)
        col_const (float): length of horizontal feature in mm
        row_const (float): length of vertical feature in mm

    Returns:
        np.ndarray: scale factor converting from pixels to mm
    """

    # Calculate the length of the two edges in pixels
    horiz_edge = np.mean([(rect_corner_coords.top_right[0] - rect_corner_coords.top_left[0]),
                               (rect_corner_coords.bot_right[0] - rect_corner_coords.bot_left[0])])
    vert_edge = np.mean([(rect_corner_coords.bot_left[1] - rect_corner_coords.top_left[1]),
                         (rect_corner_coords.bot_right[1] - rect_corner_coords.top_right[1])])

    # Calculate the pixel per mm scale factor, horiz_edge = 33mm, vert_edge = 14mm
    return np.mean([horiz_edge / col_const, vert_edge / row_const], dtype=np.float64)


def calc_img_rotation(first_pin: list, last_pin: list) -> float:
    """
    Args:
        first_pin (list): Tuple of location of first pin in (x,y)
        last_pin (list): Tuple of location of first pin in (x,y)

    Returns:
        float: rotational angle of socket (clockwise positive)
    """

    return np.arctan((first_pin[0] - last_pin[0]) / (last_pin[1] - first_pin[1]))

def mm_to_m(pin_coord: float) -> float:
    """
    Args:
        pin_coord (float): pin coordinate in millimeter

    Returns:
        float: pin coordinate in meter
    """

    # Converts mm to m
    return pin_coord/1000
