from image_processing import preproc
import matplotlib.pyplot as plt
import cv2 as cv

EMPTY = False

def main():

    while True:
        # TODO: check if there is a jpeg file present in the directory, if present, proceed
        if not EMPTY:
            # TODO: read the jpeg image and return a matrix
            break
        else:
            continue



    filename = 'files/input_files//preproc//img_preproc_1.jpg'
    img = preproc.read_file(filename)

    img_socket = img[1000:1412,1118:1271]
    print(img_socket.shape)

    cv.imwrite('files/output_files//img_cropped.jpg', img)
    cv.imwrite('files/output_files//img_socket.jpg', img_socket)

    plt.imshow(img_socket)
    plt.show()

# def img_masked(img,sample_range):
#     img[sample_range]
    img_masked = img

    for i in range(1000-10,1412):
        for j in range(1118-20,1271):
            img_masked[i,j] = img[(1042,1166)]

    cv.imwrite('files/output_files//img_masked.jpg', img_masked)

    plt.imshow(img_masked)
    plt.show()


if __name__ == '__main__':
    main()
