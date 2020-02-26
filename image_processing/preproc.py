import cv2 as cv


def read_file(file_name):
    return cv.cvtColor(cv.imread(file_name), cv.COLOR_BGR2RGB)

def crop_img(img, ylim, xlim):
    return img[ylim[0]:ylim[1],xlim[0]:xlim[1]]
