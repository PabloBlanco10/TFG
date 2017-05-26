import cv2
import math
import numpy as np
import quaternion
from PIL import Image
import scipy
from scipy import fftpack
from scipy.fftpack import fft, dct
import transformation as TF


#blocksize
B = 8
#block
xBegin, yBegin, xEnd, yEnd = 0, 0, 8, 8

imagen = Image.open('/Users/Pablo/Desktop/12.jpeg')
img = cv2.imread('/Users/Pablo/Desktop/12.jpeg')
imageWidth = imagen.size[0]
imageHeight = imagen.size[1]

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

            pixelR = r[0, 0]
            pixelG = g[0, 0]
            pixelB = b[0, 0]

            quat = quaternion.quaternion(0,pixelR,pixelG,pixelB)
            quat2 = np.array([0,pixelR,pixelG,pixelB])
            test = scipy.fftpack.dct(quat2, type=2, n=None, axis=-1, norm=None, overwrite_x=False)
            bMatrix = TF.rotation_matrix(0.0, [r[0][0], g[0][0], b[0][0]])
            quat = TF.quaternion_from_matrix([r[0][0], g[0][0], b[0][0]])

            quaternionOfR = quaternion.as_quat_array(r)
            quaternionOfG = quaternion.as_quat_array(g)
            quaternionOfB = quaternion.as_quat_array(b)
            arrayOfColors = np.concatenate((quaternionOfR,quaternionOfG,quaternionOfB), axis=0)
            print quaternionOfB
            qdct_transformR = scipy.fftpack.dct(arrayOfColors, type=2, n=None, axis=-1, norm=None, overwrite_x=False)
           # quaternionOfColors = quaternion.as_quat_array(arrayOfColors)
            #qdct_transform = scipy.fftpack.dct(quaternionOfColors, type=2, n=None, axis=-1, norm=None, overwrite_x=False)
        xBegin = 0
        xEnd = 8
        yEnd += 8
        yBegin += 8


