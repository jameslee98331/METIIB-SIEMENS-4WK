import cv2 as cv
import matplotlib.pyplot as plt
import imgproc, robot_param, config

DEBUG = True


def process(input_img):
    # 4. Pre-processing of Images

    # Crop image to include only the G120C FSAA in the image frame
    # THIS IS TO BE ADJUSTED WHEN THE VISION SYSTEM IS PUT INTO THE PRODUCTION ENVIRONMENT
    FRAME_START = config.dev_crop['START']
    FRAME_FINISH = config.dev_crop['FINISH']
    crop_rect = imgproc.draw_rect(FRAME_START, FRAME_FINISH)
    cropped_img = imgproc.crop(input_img, crop_rect)

    if DEBUG:
        plt.imshow(cropped_img)
        plt.title("cropped image")
        plt.show()

    # 5. Feature Detection
    # Apply mask over ROI (top pin)
    MASK_0_START = config.dev_mask_0['START']
    MASK_0_FINISH = config.dev_mask_0['FINISH']
    mask_0_rect = imgproc.draw_rect(MASK_0_START, MASK_0_FINISH)
    key_pts_0_centroid, key_pts_0 = imgproc.extract_feature_centroid(cropped_img, mask_0_rect)

    # Apply mask over ROI (bottom pin)
    MASK_1_START = config.dev_mask_1['START']
    MASK_1_FINISH = config.dev_mask_1['FINISH']
    mask_1_rect = imgproc.draw_rect(MASK_1_START, MASK_1_FINISH)
    key_pts_1_centroid, key_pts_1 = imgproc.extract_feature_centroid(cropped_img, mask_1_rect)

    if DEBUG:
        print(key_pts_0_centroid)
        print(key_pts_1_centroid)
        out_img = imgproc.crop(input_img, crop_rect)
        in_img = imgproc.crop(input_img, crop_rect)
        key_pts_img = imgproc.keypts_img(in_img, out_img, key_pts_0 + key_pts_1)
        plt.imshow(key_pts_img)
        plt.title("keypoints")
        plt.show()

    # 6. Offset Calculation
    # translate pixel data to mm by using a rigid key feature on the G120C FSAA (the product)
    # TODO:
    #   - find offset from reference datum as a float

    # Ranges of pixels for the 4 corners of the rigid feature (rectangle)
    X_RANGE_LEFT = config.dev_calibration_rect['X_RANGE_LEFT']
    X_RANGE_RIGHT = config.dev_calibration_rect['X_RANGE_RIGHT']
    Y_RANGE_TOP = config.dev_calibration_rect['Y_RANGE_TOP']
    Y_RANGE_BOT = config.dev_calibration_rect['Y_RANGE_BOT']
    loc, kp = imgproc.calibration_rect(cropped_img, X_RANGE_LEFT, X_RANGE_RIGHT, Y_RANGE_TOP, Y_RANGE_BOT)
    scale = imgproc.find_scale(loc, col_const=33, row_const=14)


    if DEBUG:
        print(f'pix_per_mm: {scale}')
        in_img = imgproc.crop(input_img, crop_rect)
        out_img = imgproc.crop(input_img, crop_rect)
        key_pts_img = imgproc.keypts_img(in_img, out_img, kp)
        plt.imshow(key_pts_img)
        plt.title("reference corners")
        plt.show()

    # 7. Robot control


    # TODO:
    #   - translate pixel offset to mm offset
    #   - return offset from reference datum as a float
    #   - beware of infinite loop
    #   - potential to use a IOT2020/2040 to run this code/ communicate with the


if __name__ == '__main__':

    while True:
        # 1. Integration with Automation System
        # TODO:
        #   - receive bool isReady flag from PLC when G120C FSAA is in place and clamped
        isReady = True
        if not isReady:
            continue

        # Resets flag to False to prevent loop from starting unexpectedly in the next cycle
        isReady = False

        # TODO: this section should be refactored to read files from temp memory
        #       when camera is connected in the production environment

        # img = img_capture()

        # placeholder code for reading temporary images
        filepath = 'sample_files//input//original_img.jpg'
        input_img = cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)
        process(input_img)

        # TODO: handshaking with the robot needs to be done
        try:
            robot_param.send()
        except OSError:
            break

