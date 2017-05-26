import cv2
import math
import numpy as np
import quaternion
from PIL import Image as im
import scipy
from scipy import fftpack
from scipy.fftpack import fft, dct


#blocksize
B = 8
#block
xBegin, yBegin, xEnd, yEnd = 0, 0, 8, 8


imagen = im.open('/Users/Pablo/Desktop/12.jpeg')
img = cv2.imread('/Users/Pablo/Desktop/12.jpeg')
imageWidth = imagen.size[0]
imageHeight = imagen.size[1]
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
im.fromarray(imYCbCr[:,:,Y], "L").show()
im.fromarray(imYCbCr[:,:,Cb], "L").show()
im.fromarray(imYCbCr[:,:,Cr], "L").show()



while yEnd < imageHeight:
    while xEnd < imageWidth:
        for i in range(8):
            bloque = img[xBegin:xEnd, yBegin:yEnd]
            #get rgb components
           # r,g,b = cv2.split(bloque)
            b = cv2.split(bloque)[0]
            g = cv2.split(bloque)[1]
            r = cv2.split(bloque)[2]
            xBegin += 8
            xEnd += 8

        xBegin = 0
        xEnd = 8
        yEnd += 8
        yBegin += 8