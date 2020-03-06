import cv2 as cv
import numpy as np
import config
import imgproc
import robot

PROD = False
if PROD:
    import img_capture


def process(input_img):
    # 3. Pre-processing of Images
    # Crop image to include only the G120C FSAA in the image frame
    # THIS IS TO BE ADJUSTED WHEN THE VISION SYSTEM IS PUT INTO THE PRODUCTION ENVIRONMENT
    FRAME_START = config.demo_crop['START']
    FRAME_FINISH = config.demo_crop['FINISH']
    crop_rect = imgproc.draw_rect(FRAME_START, FRAME_FINISH)
    cropped_img = imgproc.crop(input_img, crop_rect)

    # 4. Reference Calibration
    # Translate pixel data to mm by using a rigid key feature
    # TODO:
    #   - Views chequered board with known grid intervals
    #   - calculates scale
    # see https://www.learnopencv.com/camera-calibration-using-opencv/

    # BELOW 8 LINES SHOULD BE REPLACED IN THE PRODUCTION ENVIRONMENT
    # Ranges of pixels for the 4 corners of the rigid feature on the G120C FSAA (rectangle)
    X_RANGE_LEFT = config.demo_calibration_rect['X_RANGE_LEFT']
    X_RANGE_RIGHT = config.demo_calibration_rect['X_RANGE_RIGHT']
    Y_RANGE_TOP = config.demo_calibration_rect['Y_RANGE_TOP']
    Y_RANGE_BOT = config.demo_calibration_rect['Y_RANGE_BOT']
    loc, kp = imgproc.calibration_rect(cropped_img, X_RANGE_LEFT, X_RANGE_RIGHT, Y_RANGE_TOP, Y_RANGE_BOT)
    scale = imgproc.find_scale(loc, col_const=config.demo_scale_const['col'], row_const=config.demo_scale_const['row'])
    # Taking top left corner of the rectangle as reference home location
    reference_home = loc[0]

    # 5. Feature Detection and Offset Calculation
    soc = 'top_left_soc'
    pins = config.demo_pins[soc]
    key_pts_centroids = []
    pin_coords = []

    for pin in pins:
        mask_start = config.demo_pin_mask[pin]['START']
        mask_finish = config.demo_pin_mask[pin]['FINISH']
        mask_rect = imgproc.draw_rect(mask_start, mask_finish)
        key_pts_centroid, key_pts = imgproc.extract_feature_centroid(cropped_img, mask_rect)
        pin_coord = [x / scale for x in np.subtract(key_pts_centroid, reference_home)]
        key_pts_centroids.append(key_pts_centroid)
        pin_coords.append(pin_coord)

    m_to_mm_scale = 1000
    x_offset_lin = pin_coords[0][0]/m_to_mm_scale
    z_offset_lin = pin_coords[0][1]/m_to_mm_scale
    y_offset_rot = np.arctan((pin_coords[0][0]-pin_coords[-1][0])/(pin_coords[0][1]-pin_coords[-1][1]))

    return x_offset_lin, z_offset_lin, y_offset_rot


if __name__ == '__main__':
    if PROD:
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
        if PROD:
            input_img = img_capture.img_capture(video_capture)

        # PLACEHOLDER CODE FOR READING TEMPORARY IMAGES FOR DEMO PURPOSE
        if not PROD:
            filepath = 'sample_files//input//original_img.jpg'
            input_img = cv.cvtColor(cv.imread(filepath), cv.COLOR_BGR2RGB)

        # 3. to 6.
        offset = process(input_img)

        # 7. Robot control
        # TODO:
        #   - potential to use a Siemens IOT2020/2040 to run this code/communicate with the PLC

        while True:
            try:
                robot.send(offset)
                break
            except OSError:
                continue

        # If the entire testing process is complete, exit the while loop
        isComplete = False
        if isComplete:
            break

    if PROD:
        # Close connection to camera device
        video_capture.release()
