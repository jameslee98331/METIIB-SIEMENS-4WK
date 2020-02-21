import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('/input_files//IMG_4926.jpg')
plt.imshow(img)
plt.show()

# Initiate ORB detector
orb = cv.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# draw only keypoints location,not size and orientation
img2 = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
cv.imshow('keypoints',img2)
cv.waitKey(0)
