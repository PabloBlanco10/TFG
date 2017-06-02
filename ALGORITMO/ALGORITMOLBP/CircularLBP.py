import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image as im



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

def make_lbp_with_block():
    for x in range(0, len(imgCb)):
        for y in range(0, len(imgCb)):
            center = imgCb[x, y]
            top_left = get_pixel_else_0(imgCb, x - 1, y - 1)
            top_up = get_pixel_else_0(imgCb, x, y - 1)
            top_right = get_pixel_else_0(imgCb, x + 1, y - 1)
            right = get_pixel_else_0(imgCb, x + 1, y)
            left = get_pixel_else_0(imgCb, x - 1, y)
            bottom_left = get_pixel_else_0(imgCb, x - 1, y + 1)
            bottom_right = get_pixel_else_0(imgCb, x + 1, y + 1)
            bottom_down = get_pixel_else_0(imgCb, x, y + 1)

            values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                          bottom_down, bottom_left, left])

            weights = [1, 2, 4, 8, 16, 32, 64, 128]
            res = 0
            for a in range(0, len(values)):
                res += weights[a] * values[a]

            transformed_img.itemset((x, y), res)
            # transformed_imgCb.itemset((x,y), res)

        print x


path = '/Users/Pablo/Desktop/14.jpg'

# output of ycbcr.getbands() put in order
Y = 0
Cb = 1
Cr = 2

img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
imgCb = (img[:,:,Cb])
imgCr = (img[:,:,Cr])

transformed_imgCb = (imYCbCr[:,:,Cb], "L")[0]
transformed_imgCr = (imYCbCr[:,:,Cr], "L")[0]

make_lbp_with_block(transformed_imgCb)
make_lbp_with_block(transformed_imgCr)

#return transformed_imgCb, transformed_imgCr

im.fromarray(transformed_imgCb).show
im.fromarray(transformed_imgCr).show
#cv2.imshow('image', img)
#cv2.waitKey(0)
#im.fromarray(transformed_img).show()
#return im.fromarray(transformed_imgCb), im.fromarray(transformed_imgCr)

'''
cv2.imshow('thresholded image', transformed_img)
cv2.waitKey(0)


hist,bins = np.histogram(img.flatten(),256,[0,256])

cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()

plt.plot(cdf_normalized, color = 'b')
plt.hist(transformed_img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
    '''