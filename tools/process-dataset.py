import cv2
import glob
import numpy as np
from PIL import Image



desired_res = 256
desired_points = (desired_res, desired_res)



# replace with global path to your images
inputFileNames = glob.glob("/kirbys/input/*.png")
edgeFolder = "/kirbys/edge/"
colFolder = "/kirbys/col/"
trainFolder = "/kirbys/combined/train/"
valFolder = "/kirbys/combined/val/"



def GenerateCombinedImages():
    counter = 0
    for fileName in inputFileNames:
        # fileName = inputFileNames[0]

        # print filename and save img
        print(fileName)
        color_img = cv2.imread(fileName, cv2.IMREAD_UNCHANGED)

        # save col img
        cv2.imwrite(colFolder + "colkirby" + str(counter) + ".jpg", color_img)

        # convert to grayscale
        gray_image = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

        # laplace shit
        laplace = cv2.Laplacian(gray_image, cv2.CV_64F)

        # edge detection
        laplace = np.uint8(np.absolute(laplace))

        # invert grayscale
        invert = cv2.bitwise_not(laplace)

        # convert to binary black and white
        (thresh, bwimg) = cv2.threshold(invert, 225, 255, cv2.THRESH_BINARY)

        # convert from binary to RGBA
        rgba_image = cv2.cvtColor(bwimg, cv2.COLOR_GRAY2RGBA)

        # make all white pixels transparent
        for i in range(0, rgba_image.shape[0]):
            for j in range(0, rgba_image.shape[1]):
                r = rgba_image.item(i, j, 0)
                g = rgba_image.item(i, j, 1)
                b = rgba_image.item(i, j, 2)
                a = rgba_image.item(i, j, 3)

                # print(r, g, b, a)

                if r == 255 & g == 255 & b == 255:
                    rgba_image.itemset((i, j, 3), 0)


        # save edge img
        cv2.imwrite(edgeFolder + "edgekirby" + str(counter) + ".jpg", rgba_image)

        # combine imagees
        vis = np.concatenate((color_img, rgba_image), axis=1)

        #save combined image in either train or val
        if counter % 6 == 0:
            cv2.imwrite(valFolder + "" + str(counter) + ".jpg", vis)
        else:
            cv2.imwrite(trainFolder + "" + str(counter) + ".jpg", vis)

        # cv2.imshow('Example - Show image in window', invert)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        counter += 1




def ResizeImages():
    oldcolFileNames = glob.glob("/kirbys/oldcolored/*.png")
    for i in oldcolFileNames:
        print(i)
        img = cv2.imread(i)

        resize_down = cv2.resize(img, desired_points, interpolation=cv2.INTER_AREA)

        cv2.imshow('', resize_down)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



# look through all  images
def CheckImages():
    for i in inputFileNames:
        print(i)
        img = cv2.imread(i)
        cv2.imshow('', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

GenerateCombinedImages()