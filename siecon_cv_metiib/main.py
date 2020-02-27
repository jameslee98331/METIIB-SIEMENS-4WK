import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from files import file_handling
from image_processing import offset, preproc
from image_processing.features import KeyPointFeature
from robot import robot_param


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
    # The directory in which live images is stored
    img_dir = 'files/live_img//'

    # Check if there are images to be processed in the live_img/ directory
    while file_handling.dir_empty(img_dir):
        continue

    file_path = file_handling.first_img(img_dir)

    # 4. Pre-processing of Images
    input_img = preproc.read_image(file_path)

    # corner = (row, col)
    # Defined limits to include only the G120C FSAA in the image frame
    # THIS IS TO BE ADJUSTED WHEN THE VISION SYSTEM IS PUT INTO THE PRODUCTION ENVIRONMENT
    # TODO: define these values in a config.py somewhere else so it is easier for deployment
    FRAME_START = (460, 680)
    FRAME_FINISH = (3400, 2100)

    # TODO: define the namedtuple somewhere else
    rect = namedtuple('rect', 'start, finish')
    crop_rect = rect(FRAME_START, FRAME_FINISH)

    cropped_img = preproc.crop(input_img, crop_rect)

    # TODO:
    #   - increase contrast
    #   - return processed image

    # 5. Feature Detection
    rect = namedtuple('rect', 'start, finish')

    # TODO: define these values in a config.py somewhere else so it is easier for deployment
    MASK_0_START = (1180, 1040)
    MASK_0_FINISH = (1220, 1100)
    mask_0_rect = rect(MASK_0_START, MASK_0_FINISH)
    mask_0 = preproc.mask(cropped_img, mask_0_rect)

    feature = KeyPointFeature(cropped_img, mask_0)
    key_pts_0_coord = feature.keypts_coord
    key_pts_0 = feature.keypts

    # TODO: define these values in a config.py somewhere else so it is easier for deployment
    MASK_1_START = (1180, 1300)
    MASK_1_FINISH = (1220, 1360)
    mask_1_rect = rect(MASK_1_START, MASK_1_FINISH)
    mask_1 = preproc.mask(cropped_img, mask_1_rect)

    feature = KeyPointFeature(cropped_img, mask_1)
    key_pts_1_coord = feature.keypts_coord
    key_pts_1 = feature.keypts

    if DEBUG:
        key_pts_img = feature.keypts_img(cropped_img, key_pts_0 + key_pts_1)
        plt.imshow(key_pts_img)
        plt.show()

    # 6. Offset Calculation
    key_pts_0_centroid = offset.centroid(key_pts_0_coord)
    key_pts_1_centroid = offset.centroid(key_pts_1_coord)

    if DEBUG:
        print(key_pts_0_centroid)
        print(key_pts_1_centroid)

    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float

    X_RANGE_LEFT = (400, 430)
    X_RANGE_RIGHT = (1010, 1040)
    Y_RANGE_TOP = (350, 380)
    Y_RANGE_BOT = (610, 640)

    MASK_TOP_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_TOP[0])
    MASK_TOP_LEFT_FINISH = (X_RANGE_LEFT[1], Y_RANGE_TOP[1])
    mask_top_left_rect = rect(MASK_TOP_LEFT_START, MASK_TOP_LEFT_FINISH)
    mask_top_left = preproc.mask(cropped_img, mask_top_left_rect)
    feature = KeyPointFeature(cropped_img, mask_top_left)
    key_pts_top_left_coord = feature.keypts_coord
    key_pts_top_left_centroid = offset.centroid(key_pts_top_left_coord)
    key_pts_top_left = feature.keypts

    MASK_TOP_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_TOP[0])
    MASK_TOP_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_TOP[1])
    mask_top_right_rect = rect(MASK_TOP_RIGHT_START, MASK_TOP_RIGHT_END)
    mask_top_right = preproc.mask(cropped_img, mask_top_right_rect)
    feature = KeyPointFeature(cropped_img, mask_top_right)
    key_pts_top_right_coord = feature.keypts_coord
    key_pts_top_right_centroid = offset.centroid(key_pts_top_right_coord)
    key_pts_top_right = feature.keypts

    MASK_BOT_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_BOT[0])
    MASK_BOT_LEFT_END = (X_RANGE_LEFT[1], Y_RANGE_BOT[1])
    mask_bot_left_rect = rect(MASK_BOT_LEFT_START, MASK_BOT_LEFT_END)
    mask_bot_left = preproc.mask(cropped_img, mask_bot_left_rect)
    feature = KeyPointFeature(cropped_img, mask_bot_left)
    key_pts_bot_left_coord = feature.keypts_coord
    key_pts_bot_left_centroid = offset.centroid(key_pts_bot_left_coord)
    key_pts_bot_left = feature.keypts

    MASK_BOT_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_BOT[0])
    MASK_BOT_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_BOT[1])
    mask_bot_right_rect = rect(MASK_BOT_RIGHT_START, MASK_BOT_RIGHT_END)
    mask_bot_right = preproc.mask(cropped_img, mask_bot_right_rect)
    feature = KeyPointFeature(cropped_img, mask_bot_right)
    key_pts_bot_right_coord = feature.keypts_coord
    key_pts_bot_right_centroid = offset.centroid(key_pts_bot_right_coord)
    key_pts_bot_right = feature.keypts

    top_x = np.mean([(key_pts_top_right_centroid[0] - key_pts_top_left_centroid[0]),
                    (key_pts_bot_right_centroid[0] - key_pts_bot_left_centroid[0])])
    vert_y = np.mean([(key_pts_bot_left_centroid[1] - key_pts_top_left_centroid[1]),
                     (key_pts_bot_right_centroid[1] - key_pts_top_right_centroid[1])])

    pix_per_mm_0 = top_x / 33
    pix_per_mm_1 = vert_y / 14
    a = np.mean([pix_per_mm_0, pix_per_mm_1])

    if DEBUG:
        input_img = preproc.read_image(file_path)
        cropped_img = preproc.crop(input_img, crop_rect)
        key_pts_img = feature.keypts_img(cropped_img, key_pts_top_left + key_pts_top_right + key_pts_bot_left + key_pts_bot_right)
        plt.imshow(key_pts_img)
        plt.show()

    # 7. Robot control
    robot_param.send()
    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float


if __name__ == '__main__':
    # while True:
    main()
