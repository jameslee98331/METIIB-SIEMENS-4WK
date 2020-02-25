import preproc
import matplotlib.pyplot as plt


def main():
    filename = 'input_files//img_preproc_1.jpg'
    img = preproc.read_file(filename)

    x_lim = (680, 2100)
    y_lim = (460, 3400)
    img_cropped = preproc.crop_img(img, y_lim, x_lim)

    img_socket = img_cropped[1000:1412,1118:1271]
    print(img_socket.shape)

    plt.imshow(img_socket)
    plt.show()

# def img_masked(img,sample_range):
#     img[sample_range]
    for i in range(1000-10,1412):
        for j in range(1118-20,1271):
            img_cropped[i,j] = img_cropped[(1042,1166)]

    plt.imshow(img_cropped)
    plt.show()




if __name__ == '__main__':
    main()

