import cv2 as cv
import matplotlib.pyplot as plt
from files.file_handling import dir_empty, full_path
import image_processing.feature_detection as feature


def main():

    img_dir = 'files//live_img//'

    # continuously checks if there are images to be processed in the live_img directory
    while dir_empty(img_dir):
        continue

    file_path = full_path(img_dir)
    img = cv.imread(file_path)

    # draw your selected ROI on the mask image
    mask1 = feature.mask(img, start=(1180, 1040), finish=(1220, 1100))
    mask2 = feature.mask(img, start=(1180, 1300), finish=(1220, 1360))

    kp1_coord = feature.kp_coord(img, mask1)
    kp2_coord = feature.kp_coord(img, mask2)


    # print(kp1_coord)
    # print(kp2_coord)
    # print(len(kp1_coord))
    # print(len(kp2_coord))

    kp1 = feature.kp(img, mask1)
    kp2 = feature.kp(img, mask2)
    kp = kp1 + kp2

    kp_img = feature.kp_img(img, kp)

    plt.imshow(kp_img)
    plt.show()


if __name__ == '__main__':
    main()
