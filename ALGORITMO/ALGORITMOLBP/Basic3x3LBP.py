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

imagen = im.open('/Users/Pablo/Desktop/13.jpeg')
ycbcr = imagen.convert('YCbCr')

# output of ycbcr.getbands() put in order
Y = 0
Cb = 1
Cr = 2

YCbCr = list(ycbcr.getdata()) # flat list of tuples
# reshape
imYCbCr = np.reshape(YCbCr, (imagen.size[1], imagen.size[0], 3))
# Convert 32-bit elements to 8-bit
imYCbCr = imYCbCr.astype(np.uint8)

# now, display the 3 channels
#im.fromarray(imYCbCr[:,:,Y], "L").show()
im.fromarray(imYCbCr[:,:,Cb], "L").show()
im.fromarray(imYCbCr[:,:,Cr], "L").show()


img = cv2.imread('/Users/Pablo/Desktop/14.jpeg', 0)
#img = (imYCbCr[:,:,Cr], "L")[0]

transformed_img = cv2.imread('/Users/Pablo/Desktop/14.jpeg', 0)
#transformed_img = (imYCbCr[:,:,Cr], "L")[0]

for x in range(0, len(img)):
    for y in range(0, len(img[0])):
        center        = img[x,y]
        top_left      = get_pixel_else_0(img, x-1, y-1)
        top_up        = get_pixel_else_0(img, x, y-1)
        top_right     = get_pixel_else_0(img, x+1, y-1)
        right         = get_pixel_else_0(img, x+1, y )
        left          = get_pixel_else_0(img, x-1, y )
        bottom_left   = get_pixel_else_0(img, x-1, y+1)
        bottom_right  = get_pixel_else_0(img, x+1, y+1)
        bottom_down   = get_pixel_else_0(img, x,   y+1 )

        values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                      bottom_down, bottom_left, left])

        weights = [1, 2, 4, 8, 16, 32, 64, 128]
        res = 0
        for a in range(0, len(values)):
            res += weights[a] * values[a]

        transformed_img.itemset((x,y), res)

    print x

#cv2.imshow('image', img)
#cv2.waitKey(0)
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