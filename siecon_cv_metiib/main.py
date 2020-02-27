import cv2 as cv
import matplotlib.pyplot as plt
from siecon_cv_metiib.files import file_handling
from siecon_cv_metiib.image_processing import features, offset, preproc


DEBUG = True

def main():

    # 1. Integration with Automation System
    # TODO:
    #   - receive proceed flag from PLC when G120C FSAA is in place and clamped
    # proceed_FLAG = False
    # while not proceed_FLAG:
    #     continue

    # 2. Capturing image with camera
    # TODO:
    #   - taking pictures with camera
    #   - saving the image into the image directory
    #   - overwriting previous image

    # 3. File Handling
    # The directory in which live images should be stored
    img_dir = 'siecon_cv_metiib/files/live_img//'

    # continuously checks if there are images to be processed in the live_img/ directory
    while file_handling.dir_empty(img_dir):
        continue

    file_path = file_handling.full_path(img_dir)
    img = cv.imread(file_path)

    # 4. Pre-processing of Images
    # TODO:
    #   - preprocess image in live_img/ directory
    #   - crop image to size
    #   - increase contrast
    #   - return processed image
    # img = preproc.crop(img, start=(), finish=())


    # 5. Feature Detection
    # draw your selected ROI on the mask image
    mask0 = features.mask(img, start=(1180, 1040), finish=(1220, 1100))
    mask1 = features.mask(img, start=(1180, 1300), finish=(1220, 1360))

    kp0_coord = features.kp_coord(img, mask0)
    kp1_coord = features.kp_coord(img, mask1)

    if DEBUG:
        kp0 = features.kp(img, mask0)
        kp1 = features.kp(img, mask1)
        kp = kp0 + kp1
        kp_img = features.kp_img(img, kp)
        cv.imwrite('siecon_cv_metiib/files/output_files/ORB_keypoints.jpg', kp_img)
        plt.imshow(kp_img)
        plt.show()


    # 6. Offset Calculation
    centroid_0 = offset.centroid(kp0_coord)
    centroid_1 = offset.centroid(kp1_coord)

    if DEBUG:
        print(centroid_0)
        print(centroid_1)

    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float


    # 7. Robot control
    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float


if __name__ == '__main__':
    # while True:
    main()
