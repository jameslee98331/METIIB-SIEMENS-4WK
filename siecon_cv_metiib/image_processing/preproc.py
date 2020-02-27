import cv2 as cv


def read_file(file_name):
    return cv.cvtColor(cv.imread(file_name), cv.COLOR_BGR2RGB)

def crop(img, start: tuple, finish: tuple):
    return img[start[0]:finish[0], start[1]:finish[1]]
