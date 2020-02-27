import cv2 as cv


class KeyPointFeature:

    def __init__(self, img, mask):
        self.img = img

        # Initiate ORB detector
        orb = cv.ORB_create()

        # find the keypoints with ORB
        self.keypts = orb.detect(img, mask)

        # convert keypoint object to locations array
        self.keypts_coord = cv.KeyPoint_convert(self.keypts)

    def keypts_img(self, img, key_points):
        # draw only keypoints location,not size and orientation
        return cv.drawKeypoints(img, key_points, img, color=(0, 255, 0), flags=0)
