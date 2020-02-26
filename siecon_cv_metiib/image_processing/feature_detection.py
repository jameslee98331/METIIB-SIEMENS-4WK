import cv2 as cv
import numpy as np


def mask(img, start: tuple, finish: tuple):
    # create a mask image filled with zeros, the size of original image
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    return cv.rectangle(mask, start, finish, (255), thickness=-1)

def kp_coord(img, mask):
    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img, mask)

    # convert keypoint object to locations array
    return cv.KeyPoint_convert(kp)

def kp(img, mask):
    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    return orb.detect(img, mask)

def kp_img(img, kp):

    # Initiate ORB detector
    orb = cv.ORB_create()

    # compute the descriptors with ORB
    key_points, descriptors = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    return cv.drawKeypoints(img, key_points, img, color=(255, 0, 0), flags=0)
