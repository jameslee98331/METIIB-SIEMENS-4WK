import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


n=2

for i in range(1,n):
    filename = f'..//files//input_files//preproc//img_preproc_{i}.jpg'
    img = cv.imread(filename)

    # Initiate ORB detector
    orb = cv.ORB_create()

    # create a mask image filled with zeros, the size of original image
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    # draw your selected ROI on the mask image
    mask1 = cv.rectangle(mask, (1180, 1040), (1220, 1080), (255), thickness=-1)
    mask2 = cv.rectangle(mask, (1180, 1330), (1220, 1360), (255), thickness=-1)

    # find the keypoints with ORB
    kp1 = orb.detect(img, mask1)
    kp2 = orb.detect(img, mask2)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp1 + kp2)

    pts = cv.KeyPoint_convert(kp)

    # draw only keypoints location,not size and orientation
    img = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)

    output_name = f'..//files//output_files//ORB_keypoints_{i}.jpg'
    cv.imwrite(output_name,img)

    plt.imshow(img)
    plt.show()
