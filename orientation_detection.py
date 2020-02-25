import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

input_name_1 = 'C://Users//James//METIIB-SIEMENS-4WK//input_files//query//img_query_1.jpg'
input_name_2 = 'C://Users//James//METIIB-SIEMENS-4WK//input_files//train//img_train_2.jpg'

MIN_MATCH_COUNT = 10

img_query = cv.imread(input_name_1, 0)          # queryImage
img_train = cv.imread(input_name_2, 0)          # trainImage

# Initiate SIFT detector
sift = cv.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img_query,None)
kp2, des2 = sift.detectAndCompute(img_train,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img_query.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts,M)

    img2 = cv.polylines(img_train,[np.int32(dst)],True,255,3, cv.LINE_AA)

else:
    print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv.drawMatches(img_query,kp1,img_train,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()






# img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#
# # plt.imshow(img_rgb)
# # plt.show()
#
# img_gray= cv.cvtColor(img_rgb,cv.COLOR_RGB2GRAY)
# sift = cv.xfeatures2d.SIFT_create()
# kp = sift.detect(img_gray,None)
# img_kp=cv.drawKeypoints(img_gray,kp,img)
#
# output_name = 'C://Users//James//METIIB-SIEMENS-4WK//output_files//sift_keypoints.jpg'
# cv.imwrite(output_name,img)
#
#
# plt.imshow(img)
# plt.show()
#
# # Initiate ORB detector
# orb = cv.ORB_create()
#
# # find the keypoints with ORB
# kp = orb.detect(img, None)
#
# # compute the descriptors with ORB
# kp, des = orb.compute(img, kp)
#
# # draw only keypoints location,not size and orientation
# img2 = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
# plt.imshow(img2)
# plt.show()
#
#
