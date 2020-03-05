import cv2 as cv


def img_capture(vid_cap):
    video_capture = vid_cap

    # Read picture. ret === True on success
    ret, frame = video_capture.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Check success
    if not ret:
        raise Exception("Camera not connected")

    return frame
