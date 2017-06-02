import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image as im
from DB import dBInsert as DB



def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx,idy]
    except IndexError:
        return default

def make_lbp_with_block(transformed_img):
    for x in range(0, len(transformed_img)):
        for y in range(0, len(transformed_img)):
            center = transformed_img[x, y]
            top_left = get_pixel_else_0(transformed_img, x - 1, y - 1)
            top_up = get_pixel_else_0(transformed_img, x, y - 1)
            top_right = get_pixel_else_0(transformed_img, x + 1, y - 1)
            right = get_pixel_else_0(transformed_img, x + 1, y)
            left = get_pixel_else_0(transformed_img, x - 1, y)
            bottom_left = get_pixel_else_0(transformed_img, x - 1, y + 1)
            bottom_right = get_pixel_else_0(transformed_img, x + 1, y + 1)
            bottom_down = get_pixel_else_0(transformed_img, x, y + 1)

            values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                          bottom_down, bottom_left, left])

            weights = [1, 2, 4, 8, 16, 32, 64, 128]
            res = 0
            for a in range(0, len(values)):
                res += weights[a] * values[a]

            transformed_img.itemset((x, y), res)
            # transformed_imgCb.itemset((x,y), res)
        #print x
    return transformed_img

def lbp_cb_cr(path):
    # output of ycbcr.getbands() put in order
    Y = 0
    Cb = 1
    Cr = 2
    B = 8 #blocksize


    img = cv2.imread(path)
    #img1 = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    #cv2.imshow('imageBGR', img2)
    #cv2.imshow('imageRGB', img1)
    #cv2.waitKey(0)

    imgCb = (img[:, :, Cb])
    imgCr = (img[:, :, Cr])

    width = len(img[0])
    height = len(img)

    x = divmod(width,B)[1]
    y = divmod(height, B)[1]
    xBegin = x/2
    yBegin = y/2
    xEnd = xBegin + B
    yEnd = yBegin + B

    transformed_imgCb = (img[:, :, Cb], "L")[0]
    transformed_imgCr = (img[:, :, Cr], "L")[0]

    while(yEnd <= height):
        while(xEnd <= width):
            bloqueCb = transformed_imgCb[yBegin:yEnd, xBegin:xEnd]
            bloqueCr = transformed_imgCr[yBegin:yEnd, xBegin:xEnd]

            bloqueCb = make_lbp_with_block(bloqueCb)
            bloqueCr = make_lbp_with_block(bloqueCr)

            #wavelet
            InsWaveLBP = DB.WaveletsLBP(bloqueCb,
                                     bloqueCr)  # Modifica la funcion wavelets para trabajar con la matriz de la imagen

            print "X: %d" %xEnd
            xBegin += 8
            xEnd += 8

        print "Y: %d" %yEnd
        xBegin = x/2
        xEnd = xBegin + B
        yBegin += B
        yEnd += B

    #transformed_imgCb = make_lbp_with_block(transformed_imgCb)
    #transformed_imgCr = make_lbp_with_block(transformed_imgCr)

    return im.fromarray(transformed_imgCb), im.fromarray(transformed_imgCr)