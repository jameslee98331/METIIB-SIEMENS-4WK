import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
import file_handling
from image_processing import offset, preproc, features
import robot_param

DEBUG = True


def main():

    # 1. Integration with Automation System
    # TODO:
    #   - receive proceed flag from PLC when G120C FSAA is in place and clamped
    #   proceed_FLAG = False
    #   while not proceed_FLAG:
    #       continue

    # 2. Capturing image with camera
    # TODO:
    #   - taking pictures with camera
    #   - saving the image into temporary memory (RAM)
    #   - overwriting previous image

    # 3. File Handling
    # TODO: this section should be refactored to read files from temp memory
    #       when camera is connected in the production environment
    # The directory captured image is stored
    img_dir = 'live_img//'

    # Check if img present in the live_img/ directory, continue when img exists
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

    # Apply mask over ROI (top pin)
    mask_0_rect = rect(MASK_0_START, MASK_0_FINISH)
    mask_0 = preproc.mask(cropped_img, mask_0_rect)

    # Find locations of keypoints detected under mask 0 (top pin)
    key_pts_0_coord, key_pts_0 = features.keypts(cropped_img, mask_0)

    # TODO: define these values in a config.py somewhere else so it is easier for deployment
    MASK_1_START = (1180, 1300)
    MASK_1_FINISH = (1220, 1360)

    # Apply mask over ROI (bottom pin)
    mask_1_rect = rect(MASK_1_START, MASK_1_FINISH)
    mask_1 = preproc.mask(cropped_img, mask_1_rect)

    # Find locations of keypoints detected under mask 1 (bottom pin)
    key_pts_1_coord, key_pts_1 = features.keypts(cropped_img, mask_1)

    if DEBUG:
        key_pts_img = features.keypts_img(cropped_img, key_pts_0 + key_pts_1)
        plt.imshow(key_pts_img)
        plt.show()

    # 6. Offset Calculation
    key_pts_0_centroid = offset.centroid(key_pts_0_coord)
    key_pts_1_centroid = offset.centroid(key_pts_1_coord)

    if DEBUG:
        print(key_pts_0_centroid)
        print(key_pts_1_centroid)

    # TODO:
    #   - translate pixel to mm by using a rigid key feature on the G120C FSAA (the product)
    #   - find offset from reference datum as a float

    # Ranges of pixels for the 4 corners of the rigid feature (rectangle)
    X_RANGE_LEFT = (400, 430)
    X_RANGE_RIGHT = (1010, 1040)
    Y_RANGE_TOP = (350, 380)
    Y_RANGE_BOT = (610, 640)

    # Extract feature of top left corner
    MASK_TOP_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_TOP[0])
    MASK_TOP_LEFT_FINISH = (X_RANGE_LEFT[1], Y_RANGE_TOP[1])
    mask_top_left_rect = rect(MASK_TOP_LEFT_START, MASK_TOP_LEFT_FINISH)
    mask_top_left = preproc.mask(cropped_img, mask_top_left_rect)
    key_pts_top_left_coord, key_pts_top_left = features.keypts(cropped_img, mask_top_left)
    key_pts_top_left_centroid = offset.centroid(key_pts_top_left_coord)

    # Extract feature of top right corner
    MASK_TOP_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_TOP[0])
    MASK_TOP_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_TOP[1])
    mask_top_right_rect = rect(MASK_TOP_RIGHT_START, MASK_TOP_RIGHT_END)
    mask_top_right = preproc.mask(cropped_img, mask_top_right_rect)
    key_pts_top_right_coord, key_pts_top_right = features.keypts(cropped_img, mask_top_right)
    key_pts_top_right_centroid = offset.centroid(key_pts_top_right_coord)

    # Extract feature of bottom left corner
    MASK_BOT_LEFT_START = (X_RANGE_LEFT[0], Y_RANGE_BOT[0])
    MASK_BOT_LEFT_END = (X_RANGE_LEFT[1], Y_RANGE_BOT[1])
    mask_bot_left_rect = rect(MASK_BOT_LEFT_START, MASK_BOT_LEFT_END)
    mask_bot_left = preproc.mask(cropped_img, mask_bot_left_rect)
    key_pts_bot_left_coord, key_pts_bot_left = features.keypts(cropped_img, mask_bot_left)
    key_pts_bot_left_centroid = offset.centroid(key_pts_bot_left_coord)

    # Extract feature of bottom right corner
    MASK_BOT_RIGHT_START = (X_RANGE_RIGHT[0], Y_RANGE_BOT[0])
    MASK_BOT_RIGHT_END = (X_RANGE_RIGHT[1], Y_RANGE_BOT[1])
    mask_bot_right_rect = rect(MASK_BOT_RIGHT_START, MASK_BOT_RIGHT_END)
    mask_bot_right = preproc.mask(cropped_img, mask_bot_right_rect)
    key_pts_bot_right_coord, key_pts_bot_right = features.keypts(cropped_img, mask_bot_right)
    key_pts_bot_right_centroid = offset.centroid(key_pts_bot_right_coord)

    # Calculate the length of the two edges in pixels
    top_edge = np.mean([(key_pts_top_right_centroid[0] - key_pts_top_left_centroid[0]),
                    (key_pts_bot_right_centroid[0] - key_pts_bot_left_centroid[0])])
    vert_edge = np.mean([(key_pts_bot_left_centroid[1] - key_pts_top_left_centroid[1]),
                     (key_pts_bot_right_centroid[1] - key_pts_top_right_centroid[1])])

    # Calculate the pixel per mm scale factor, top_edge = 33mm, vert_edge = 14mm
    pix_per_mm_0 = top_edge / 33
    pix_per_mm_1 = vert_edge / 14
    pix_per_mm = np.mean([pix_per_mm_0, pix_per_mm_1])

    if DEBUG:
        input_img = preproc.read_image(file_path)
        cropped_img = preproc.crop(input_img, crop_rect)
        key_pts_img = features.keypts_img(cropped_img, key_pts_top_left + key_pts_top_right + key_pts_bot_left + key_pts_bot_right)
        plt.imshow(key_pts_img)
        plt.show()

    # 7. Robot control
    robot_param.send()
    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float
    #   - beware of infinite loop


if __name__ == '__main__':
    # while True:
    main()
