import cv2 as cv


def img_capture():
    video_capture = cv.VideoCapture(0)

    try:
        # Read picture. ret === True on success
        ret, frame = video_capture.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return frame

    except:
        # Check success
        if not video_capture.isOpened():
            return False

    finally:
        # Close device
        video_capture.release()
        cv.destroyAllWindows()
