import time
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import config
import imgproc
import robot_param
# import img_capture


def process(input_img):
    # 3. Pre-processing of Images
    # Crop image to include only the G120C FSAA in the image frame
    # THIS IS TO BE ADJUSTED WHEN THE VISION SYSTEM IS PUT INTO THE PRODUCTION ENVIRONMENT
    FRAME_START = config.dev_crop['START']
    FRAME_FINISH = config.dev_crop['FINISH']
    crop_rect = imgproc.draw_rect(FRAME_START, FRAME_FINISH)
    cropped_img = imgproc.crop(input_img, crop_rect)

    # 4. Camera Calibration
    # Translate pixel data to mm by using a rigid key feature
    # TODO:
    #   - Views chequered board with known grid intervals
    #   - calculates scale
    # see https://www.learnopencv.com/camera-calibration-using-opencv/

    # BELOW 8 LINES SHOULD BE REPLACED IN THE PRODUCTION ENVIRONMENT
    # Ranges of pixels for the 4 corners of the rigid feature on the G120C FSAA (rectangle)
    X_RANGE_LEFT = config.dev_calibration_rect['X_RANGE_LEFT']
    X_RANGE_RIGHT = config.dev_calibration_rect['X_RANGE_RIGHT']
    Y_RANGE_TOP = config.dev_calibration_rect['Y_RANGE_TOP']
    Y_RANGE_BOT = config.dev_calibration_rect['Y_RANGE_BOT']
    loc, kp = imgproc.calibration_rect(cropped_img, X_RANGE_LEFT, X_RANGE_RIGHT, Y_RANGE_TOP, Y_RANGE_BOT)
    scale = imgproc.find_scale(loc, col_const=33, row_const=14)
    reference_location = loc[0]

    # 5. Feature Detection
    # Apply mask over ROI (L1)
    MASK_2_START = config.dev_mask_2['START']
    MASK_2_FINISH = config.dev_mask_2['FINISH']
    mask_2_rect = imgproc.draw_rect(MASK_2_START, MASK_2_FINISH)
    key_pts_2_centroid, key_pts_2 = imgproc.extract_feature_centroid(cropped_img, mask_2_rect)

    # Apply mask over ROI (L2N)
    MASK_3_START = config.dev_mask_3['START']
    MASK_3_FINISH = config.dev_mask_3['FINISH']
    mask_3_rect = imgproc.draw_rect(MASK_3_START, MASK_3_FINISH)
    key_pts_3_centroid, key_pts_3 = imgproc.extract_feature_centroid(cropped_img, mask_3_rect)

    # Apply mask over ROI (L3)
    MASK_4_START = config.dev_mask_4['START']
    MASK_4_FINISH = config.dev_mask_4['FINISH']
    mask_4_rect = imgproc.draw_rect(MASK_4_START, MASK_4_FINISH)
    key_pts_4_centroid, key_pts_4 = imgproc.extract_feature_centroid(cropped_img, mask_4_rect)

    # Apply mask over ROI (GROUND)
    MASK_5_START = config.dev_mask_5['START']
    MASK_5_FINISH = config.dev_mask_5['FINISH']
    mask_5_rect = imgproc.draw_rect(MASK_5_START, MASK_5_FINISH)
    key_pts_5_centroid, key_pts_5 = imgproc.extract_feature_centroid(cropped_img, mask_5_rect)

    kp = key_pts_2 + key_pts_3 + key_pts_4 + key_pts_5
    kp_img = imgproc.keypts_img(cropped_img, kp)
    cv.imwrite('sample_files//output//ORB_keypoints_4.jpg', kp_img)

    # 6. Offset Calculation
    # Find pin L1
    pin_2_loc = tuple(np.subtract(key_pts_2_centroid, reference_location))
    pin_2_loc = tuple([x / scale for x in pin_2_loc])

    # Find pin L2N
    pin_3_loc = tuple(np.subtract(key_pts_3_centroid, reference_location))
    pin_3_loc = tuple([x / scale for x in pin_3_loc])

    # Find pin L3
    pin_4_loc = tuple(np.subtract(key_pts_4_centroid, reference_location))
    pin_4_loc = tuple([x / scale for x in pin_4_loc])

    # Find pin GROUND
    pin_5_loc = tuple(np.subtract(key_pts_5_centroid, reference_location))
    pin_5_loc = tuple([x / scale for x in pin_5_loc])

    return (pin_2_loc[0]/1000, pin_2_loc[1]/1000, np.arctan((pin_2_loc[0]-pin_5_loc[0])/(pin_2_loc[1]-pin_5_loc[1]))), kp_img


if __name__ == '__main__':
    while True:
        # 1. Integration with Automation System
        # TODO:
        #   - code to communicate with PLC and asks for clamp status
        #   - receive bool isClamp flag from PLC when G120C FSAA is in place and clamped
        # e.g. isClamped = plc.request_status()
        isClamped = True
        if not isClamped:
            continue

        # 2. Image capture
        # FOLLOWING LINE SHOULD BE USED INSTEAD IN THE PRODUCTION ENVIRONMENT:
        # input_img = img_capture.img_capture()

        # Placeholder code for reading temporary images for demo
        filepath = 'sample_files//input//original_img.jpg'
        input_img = cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)

        # 3. to 6.
        offset, kp_img = process(input_img)
        print(offset)
        plt.imshow(kp_img)
        plt.show()

        # 7. Robot control
        # TODO:
        #   - beware of infinite loop
        #   - potential to use a IOT2020/2040 to run this code/ communicate with the

        while True:
            try:
                robot_param.send(offset)
                break
            except OSError:
                continue

        while isClamped:
            # 1. Integration with Automation System
            # TODO:
            #   - receive bool isClamped flag from PLC to check if G120C FSAA is STILL in place and clamped
            #   - wait until isClamped is False (G120C FSAA has departed)
            # e.g. isClamped = plc.request_status()
            time.sleep(0.1)
