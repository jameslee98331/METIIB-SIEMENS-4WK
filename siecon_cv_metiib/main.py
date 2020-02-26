import cv2 as cv
import matplotlib.pyplot as plt
from siecon_cv_metiib.files.file_handling import dir_empty, full_path
from siecon_cv_metiib.image_processing import features
from siecon_cv_metiib.image_processing import offset


def main():

    img_dir = 'files/live_img//'

    # continuously checks if there are images to be processed in the live_img directory
    while dir_empty(img_dir):
        continue

    file_path = full_path(img_dir)
    img = cv.imread(file_path)

    # draw your selected ROI on the mask image
    mask0 = features.mask(img, start=(1180, 1040), finish=(1220, 1100))
    mask1 = features.mask(img, start=(1180, 1300), finish=(1220, 1360))

    kp0_coord = features.kp_coord(img, mask0)
    kp1_coord = features.kp_coord(img, mask1)

    kp0 = features.kp(img, mask0)
    kp1 = features.kp(img, mask1)
    kp = kp0 + kp1

    centroid_0 = offset.centroid(kp0_coord)
    centroid_1 = offset.centroid(kp1_coord)

    kp_img = features.kp_img(img, kp)
    plt.imshow(kp_img)
    plt.show()

    print(centroid_0)
    print(centroid_1)


if __name__ == '__main__':
    main()
