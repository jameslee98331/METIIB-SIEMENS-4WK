import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


for i in range(1,4):
    filename = f'input_files//preproc//img_preproc_{i}.jpg'
    img = cv.imread(filename)

    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img, None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # kp_0 = kp[0]
    # # print(kp_0)
    # # print(kp)
    # # print(type(kp_0))
    # # print(type(kp))

    pts = cv.KeyPoint_convert(kp)

    # draw only keypoints location,not size and orientation
    img = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)

    output_name = f'output_files//ORB_keypoints_{i}.jpg'
    cv.imwrite(output_name,img)

    plt.imshow(img)
    plt.show()
