import cv2
import numpy as np
from PIL import Image

#opencv PIL buscar QDCT

#blocksize
B = 8
xBegin = 0
yBegin = 0
xEnd = 8
yEnd = 8


imagen = Image.open('/Users/Pablo/Desktop/12.jpeg')
img = cv2.imread('/Users/Pablo/Desktop/12.jpeg')
print img
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
            print bloque
        xBegin = 0
        xEnd = 8
        yEnd += 8
        yBegin += 8

#bloque = img[xBegin:xEnd, yBegin:yEnd]
#bloque = img[np.ix_([0, 7], [0, 7])]
#print bloque




r,g,b = cv2.split(img)

img8x8 = np.array(img).reshape(8,8)

print r


#recibe lista de imagenes o solo una imagen?
def algorithm(img):

    #move block
    for r in range(0, img.shape[0] - B, B):
        for c in range(0, img.shape[1] - B, B):
            window = img[r:r + B, c:c + B]
            color = createColorComponents(window)
          #  makeQdctTransform(color)


#return RGB of block
def createColorComponents(filename, idImage):
    img1 = cv2.imread(filename, cv2.CV_LOAD_IMAGE_UNCHANGED)
    h, w = np.array(img1.shape[:2]) / B * B
    img1 = img1[:h, :w]
    # Convert BGR to RGB
    img2 = np.zeros(img1.shape, np.uint8)
    img2[:, :, 0] = img1[:, :, 2] #R
    img2[:, :, 1] = img1[:, :, 1] #G
    img2[:, :, 2] = img1[:, :, 0] #B
    return img2


#def makeQdctTransform():
