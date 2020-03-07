import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import config
import imgproc
import robot
import img_capture

DEBUG = True


def process(input_image):
    # 3. Pre-processing of Images
    # Crop image to include only the G120C FSAA in the image frame
    # THIS IS TO BE ADJUSTED WHEN THE VISION SYSTEM IS PUT INTO THE PRODUCTION ENVIRONMENT
    frame_start = config.demo_crop['start']
    frame_finish = config.demo_crop['finish']
    crop_rect = imgproc.draw_rect(frame_start, frame_finish)
    cropped_img = imgproc.crop(input_image, crop_rect)

    # 4. Reference Calibration
    # Translate pixel data to mm by using a rigid key feature
    # TODO:
    #   - Views chequered board with known grid intervals
    #   - calculates scale
    # see https://www.learnopencv.com/camera-calibration-using-opencv/

    # BELOW 8 LINES SHOULD BE REPLACED IN THE PRODUCTION ENVIRONMENT
    # Ranges of pixels for the 4 corners of the rigid feature on the G120C FSAA (rectangle)
    x_range_left = config.demo_calibration_rect['x_range_left']
    x_range_right = config.demo_calibration_rect['x_range_right']
    y_range_top = config.demo_calibration_rect['y_range_top']
    y_range_bot = config.demo_calibration_rect['y_range_bot']
    rect_corner_coords, kp = imgproc.calibration_rect(cropped_img, x_range_left, x_range_right, y_range_top,
                                                      y_range_bot)
    scale = imgproc.find_scale(rect_corner_coords, col_const=config.demo_scale_const['col'],
                               row_const=config.demo_scale_const['row'])
    # Taking top left corner of the rectangle as reference home location
    reference_home = rect_corner_coords.top_left

    # 5. Feature Detection and Offset Calculation
    soc = 'top_left_soc'
    pins = config.demo_pin_mask[soc]
    key_pts_centroids = []
    pin_coords = []
    key_pts_all = []

    for value in pins.values():
        mask_start = value['start']
        mask_finish = value['finish']
        mask_rect = imgproc.draw_rect(mask_start, mask_finish)
        key_pts_centroid, key_pts = imgproc.extract_feature_centroid(cropped_img, mask_rect)
        pin_coord = [x / scale for x in np.subtract(key_pts_centroid, reference_home)]
        key_pts_centroids.append(key_pts_centroid)
        pin_coords.append(pin_coord)
        key_pts_all.extend(key_pts)

    x_offset_lin = imgproc.mm_to_m(pin_coords[0][0])
    z_offset_lin = imgproc.mm_to_m(pin_coords[0][1])
    rotation = imgproc.calc_img_rotation(pin_coords[0], pin_coords[-1])

    if DEBUG:
        print(key_pts_centroids)
        print(pin_coords)
        print(key_pts_all)
        kp_img = imgproc.keypts_img(cropped_img, key_pts_all)
        plt.imshow(kp_img)
        plt.show()
        print((x_offset_lin, z_offset_lin, rotation))

    return x_offset_lin, z_offset_lin, rotation


if __name__ == '__main__':
    if not DEBUG:
        # Initialise cameras
        video_capture = cv.VideoCapture(0)

    while True:
        # 1. Integration with Automation System
        # TODO:
        #   - code to communicate with PLC and asks for clamp status
        #   - receive bool isClamp flag from PLC when new G120C FSAA is in place and clamped
        # e.g. isClamped = plc.request_status()

        # Placeholder code for assuming product is clamped
        isClamped = True

        if not isClamped:
            continue

        isClamped = False

        # 2. Image capture
        if not DEBUG:
            input_img = img_capture.img_capture(video_capture)

        # PLACEHOLDER CODE FOR READING TEMPORARY IMAGES FOR DEMO PURPOSE
        else:
            filepath = 'sample_files//input//original_img.jpg'
            input_img = cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)

        # 3. to 6.
        x_offset_lin, z_offset_lin, rotation = process(input_img)

        # 7. Robot control
        # TODO:
        #   - potential to use a Siemens IOT2020/2040 to run this code/communicate with the PLC
        robot.send(x_offset_lin, z_offset_lin, rotation)

        # If the entire testing process is complete, exit the while loop
        isComplete = True
        if isComplete:
            break

    if not DEBUG:
        # Close connection to camera device
        video_capture.release()
