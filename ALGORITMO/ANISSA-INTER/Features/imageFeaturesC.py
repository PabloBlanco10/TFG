from scipy import stats, ndimage, fftpack
import multiprocessing
import numpy
import time
import os
import glob
#from scipy.misc import imread
import pywt
from Features import ColorFeat
from Features import WaveFeat
from Features import WaveSmartFeat
from Features import IQMFeat
from Features import funcionesC
from PRNU import prnu
from Exception.exception import GenException

#Para evitar el error: "AccessInit: hash collision: 3 for both 1 and 1"
try:
    from PIL import Image, ImageStat
except ImportError:
    import Image
    import ImageStat



class imageFeatures:

    def averagePixelValue(self, statImage):
        return statImage.mean

    #Devuelve un ndarray con el contenido de las tres bandas de la imagen
    """
    def imageToMatriz2(self, image):
        x,y = image.size
        matriz = numpy.empty([3,y,x], dtype=numpy.uint8)
        for i in range(y):
            for j in range(x):
                vR,vG,vB = image.getpixel((j,i))
                matriz[0,i,j] = vR
                matriz[1,i,j] = vG
                matriz[2,i,j] = vB
        return matriz
    """

    def imageToMatriz(self, img):
        try:
            im = numpy.asarray(img)
            #im = imread(im)
            im = numpy.swapaxes(im, 0, 2)
            im = numpy.swapaxes(im, 1, 2)
            return im
        except GenException, e:
            raise e

    def rgbPairsCorrelation(self, imagen):
        try:
            rg = funcionesC.pearson(imagen[0],imagen[1])
            rb = funcionesC.pearson(imagen[0],imagen[2])
            bg = funcionesC.pearson(imagen[1],imagen[2])
            return [rg, rb, bg]
        except GenException, e:
            raise e

    def rgbPairsEnergyRatio(self, statImage):
        try:
            energyR, energyG, energyB = statImage.sum #supongo que la energia es la suma de las componentes de cada banda
            energyR2 = energyR**2
            energyG2 = energyG**2
            energyB2 = energyB**2
            E1 = energyG2/energyB2
            E2 = energyG2/energyR2
            E3 = energyB2/energyR2
            return [E1,E2,E3]
        except GenException, e:
            raise e

    def waveletDomainStatistics(self, imagen):
        try:
            Aprox, Details = pywt.dwt2( imagen[0], pywt.Wavelet('haar') )
            HorizDetail, VertDetail, DiagDetail = Details
            HorizDetail = pywt.qmf(HorizDetail)
            VertDetail = pywt.qmf(VertDetail)
            DiagDetail = pywt.qmf(DiagDetail)
            rH = HorizDetail.mean()
            rV = VertDetail.mean()
            rD = DiagDetail.mean()
            Aprox, Details = pywt.dwt2( imagen[1], pywt.Wavelet('haar') )
            HorizDetail, VertDetail, DiagDetail = Details
            HorizDetail = pywt.qmf(HorizDetail)
            VertDetail = pywt.qmf(VertDetail)
            DiagDetail = pywt.qmf(DiagDetail)
            gH = HorizDetail.mean()
            gV = VertDetail.mean()
            gD = DiagDetail.mean()
            Aprox, Details = pywt.dwt2( imagen[2], pywt.Wavelet('haar') )
            HorizDetail, VertDetail, DiagDetail = Details
            HorizDetail = pywt.qmf(HorizDetail)
            VertDetail = pywt.qmf(VertDetail)
            DiagDetail = pywt.qmf(DiagDetail)
            bH = HorizDetail.mean()
            bV = VertDetail.mean()
            bD = DiagDetail.mean()

            return rH,rV,rD, gH,gV,gD, bH,bV,bD
        except GenException, e:
            raise e

    def gaussianFilter(self, image, imagen, sigma, r):
        """Genero el nucleo gaussiano"""
        #print "Aplicando filtro gaussiano..."
        try:
            e = numpy.e
            pi = numpy.pi
            tamNucleo = r*2+1
            nucleo = numpy.empty([tamNucleo,tamNucleo])
            suma = 0
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    g = (1/(2*pi*(sigma**2)))*e**-((float(i**2+j**2))/(2*(sigma**2)))
                    nucleo[i+r,j+r] = g
                    suma = suma + g
            #Normalizo
            for i in range(tamNucleo):
                for j in range(tamNucleo):
                    nucleo[i,j] = nucleo[i,j] / suma


            """Aplico la transformacion"""
            x,y = image.size
            resultado = numpy.empty([3,y,x], dtype=numpy.uint8)
            funcionesC.gauss(imagen, nucleo, resultado)


            """
            #Pruebas
            for i in range(0,y):
                for j in range(0,x):
                    image.putpixel((j,i),(resultado[0,i,j],resultado[1,i,j],resultado[2,i,j]))
            image.save("C:\Users\Sergio\Desktop\Fotos\prueba.jpg")"""

            return resultado
        except GenException, e:
            raise e

    def neighborDistributionCenterOfMass(self, imagen):
        try:
            ndR = numpy.zeros(256, dtype=numpy.int)
            ndG = numpy.zeros(256, dtype=numpy.int)
            ndB = numpy.zeros(256, dtype=numpy.int)

            funcionesC.neighborDistribution(imagen[0], ndR)
            funcionesC.neighborDistribution(imagen[1], ndG)
            funcionesC.neighborDistribution(imagen[2], ndB)

            comR = ndimage.measurements.center_of_mass(ndR)
            comG = ndimage.measurements.center_of_mass(ndG)
            comB = ndimage.measurements.center_of_mass(ndB)

            return [comR[0], comG[0], comB[0]]
        except GenException, e:
            raise e



    def hvsMeasures(self,  imagenO, imagenS):
        try:
            #Paso la matrices a float
            uR = imagenO[0].astype(float)
            uG = imagenO[1].astype(float)
            uB = imagenO[2].astype(float)
            uR2 = imagenS[0].astype(float)
            uG2 = imagenS[1].astype(float)
            uB2 = imagenS[2].astype(float)

            #Calculo la matriz U
            uR = fftpack.dct(uR)
            uG = fftpack.dct(uG)
            uB = fftpack.dct(uB)
            uR2 = fftpack.dct(uR2)
            uG2 = fftpack.dct(uG2)
            uB2 = fftpack.dct(uB2)

            funcionesC.bucle1HVS(uR,uG,uB,uR2,uG2,uB2)

            uR = fftpack.idct(uR)
            uG = fftpack.idct(uG)
            uB = fftpack.idct(uB)
            uR2 = fftpack.idct(uR2)
            uG2 = fftpack.idct(uG2)
            uB2 = fftpack.idct(uB2)

            #Calculo del NAE y del L2 norm
            res = funcionesC.bucle2HVS(uR,uG,uB,uR2,uG2,uB2)

            return res
        except GenException, e:
            raise e

    def discreteFourierTransform(self, dataImage, nfil, ncol):
        try:
            dft = numpy.empty([3,nfil,ncol], dtype=numpy.complex)
            dft[0] = numpy.fft.fft2(dataImage[0])
            dft[1] = numpy.fft.fft2(dataImage[1])
            dft[2] = numpy.fft.fft2(dataImage[2])
            return dft
        except GenException, e:
            raise e

    def weightedSpectralDistance(self, spectralP, spectralM, lambd):
        try:
            wsd1 = lambd*spectralM[0] + (1-lambd)*spectralP[0]
            wsd2 = lambd*spectralM[1] + (1-lambd)*spectralP[1]
            wsd3 = lambd*spectralM[2] + (1-lambd)*spectralP[2]
            return [wsd1, wsd2, wsd3]
        except GenException, e:
            raise e

    def medianBlockFeatures(self, imagenO, imagenS, blockSize, gamma, lambd):
        try:
            finalizado = False
            M,N = imagenO.shape[1], imagenO.shape[2]
            posX, posY = 0,0
            list1R, list1G, list1B = [],[],[]
            list2R, list2G, list2B = [],[],[]
            list3R, list3G, list3B = [],[],[]

            while(not finalizado):
                resX, resY, nextX, nextY = funcionesC.siguienteBloque(posX, posY, N, M, blockSize)
                if(nextY>=M):
                    finalizado = True

                if(resX-posX==blockSize-1 and resY-posY==blockSize-1):   #solo admito bloques de tamano blockSize X blockSize
                    dftO = self.discreteFourierTransform([imagenO[0,posY:resY+1,posX:resX+1], imagenO[1,posY:resY+1,posX:resX+1], imagenO[2,posY:resY+1,posX:resX+1]], resY-posY+1, resX-posX+1)
                    dftS = self.discreteFourierTransform([imagenS[0,posY:resY+1,posX:resX+1], imagenS[1,posY:resY+1,posX:resX+1], imagenS[2,posY:resY+1,posX:resX+1]], resY-posY+1, resX-posX+1)

                    res = funcionesC.bucleMBF(dftO,dftS,gamma,lambd)

                    list1R.append(res[0])
                    list1G.append(res[1])
                    list1B.append(res[2])
                    list2R.append(res[3])
                    list2G.append(res[4])
                    list2B.append(res[5])
                    list3R.append(res[6])
                    list3G.append(res[7])
                    list3B.append(res[8])

                posX, posY = nextX, nextY


            medianaR1 = numpy.median(list1R)
            medianaG1 = numpy.median(list1G)
            medianaB1 = numpy.median(list1B)
            medianaR2 = numpy.median(list2R)
            medianaG2 = numpy.median(list2G)
            medianaB2 = numpy.median(list2B)
            medianaR3 = numpy.median(list3R)
            medianaG3 = numpy.median(list3G)
            medianaB3 = numpy.median(list3B)

            return [medianaR1,medianaG1,medianaB1,medianaR2,medianaG2,medianaB2,medianaR3,medianaG3,medianaB3]
        except GenException, e:
            raise e


    def getAllFeatures(self, imagePath):
        try:
            inicioTotal = time.time()
            path = os.path.join(imagePath, "*.jpg")
            listaImagenes = glob.glob(path)
            for i in range(len(listaImagenes)):
                inicio = time.time()

                lista = self.caracteristicas(listaImagenes[i])

                fin = time.time()
                tiempo_total = fin - inicio
                print "Tiempo " + listaImagenes[i] + ": " + str(tiempo_total) + " segundos"

            finTotal = time.time()
            tiempo_total2 = finTotal - inicioTotal
            print "Tiempo total: " + str(tiempo_total2) + " segundos"
        except GenException, e:
            raise e

    def caracteristicas(self, imagePath):
        try:
            image = Image.open(imagePath)
            M,N = image.size
            statImage = ImageStat.Stat(image)
            imagenO = self.imageToMatriz(imagePath)

            lista = self.averagePixelValue(statImage)
            lista += self.rgbPairsCorrelation(imagenO)
            lista += self.neighborDistributionCenterOfMass(imagenO)
            lista += self.rgbPairsEnergyRatio(statImage)
            lista += self.waveletDomainStatistics(imagenO)

            imagenS = self.gaussianFilter(image, imagenO, 0.5, 1)

            lista += funcionesC.minkowskyMetric(imagenO, imagenS, 1)
            lista += funcionesC.minkowskyMetric(imagenO, imagenS, 2)
            lista += funcionesC.normalizedCrossCorrelation(imagenO, imagenS)
            lista += funcionesC.structuralContent(imagenO, imagenS)
            lista += self.hvsMeasures(imagenO, imagenS)
            lista += funcionesC.laplacianMeanSquareError(imagenO, imagenS)
            lista.append(funcionesC.czekonowskyDistance(imagenO, imagenS))

            mbf = self.medianBlockFeatures(imagenO, imagenS, 32, 2, 2.5*(10**-5))


            dftO = self.discreteFourierTransform(imagenO,N,M)
            dftS = self.discreteFourierTransform(imagenS,N,M)
            sp = funcionesC.spectralPhase(dftO, dftS)
            lista += sp
            sm = funcionesC.spectralMagnitude(dftO, dftS)
            lista += sm
            dftO = None
            dftS = None
            lista += self.weightedSpectralDistance(sp, sm, 2.5*(10**-5))

            lista += mbf

            return lista
        except GenException, e:
            raise e

    def Color_Features(self, image):
        try:
            Color_Feat = ColorFeat.ColorFeat()

            statImage = ImageStat.Stat(image)
            imagenO = self.imageToMatriz(image)

            Color_Feat.averagePixelValue = self.averagePixelValue(statImage)
            Color_Feat.rgbPairsCorrelation = self.rgbPairsCorrelation(imagenO)
            Color_Feat.neighborDistributionCenterOfMass = self.neighborDistributionCenterOfMass(imagenO)
            Color_Feat.rgbPairsEnergyRatio= self.rgbPairsEnergyRatio(statImage)

            return Color_Feat
        except GenException, e:
            raise e

    def Wavelets_Features(self, image):
        try:
            Wave_Feat = WaveFeat.WaveFeat()
            imagenO = self.imageToMatriz(image)

            rH, rV, rD, gH, gV, gD, bH, bV, bD = self.waveletDomainStatistics(imagenO)
            Wave_Feat.rH = rH
            Wave_Feat.rV = rV
            Wave_Feat.rD = rD
            Wave_Feat.gH = gH
            Wave_Feat.gV = gV
            Wave_Feat.gD = gD
            Wave_Feat.bH = bH
            Wave_Feat.bV = bV
            Wave_Feat.bD = bD
            return Wave_Feat
            #return Feat_averagePixelValue
        except GenException, e:
            raise e

    def WaveletsSmart_Features(self, imageArray):
        try:
            WaveSmart_Feat = WaveSmartFeat.WaveSmartFeat()

            features, numberOfBands = prnu.extractWaveletsFeatures(imageArray)
            #BXWMY Band X, wavelet component (H, V, D), absolute central moment Y
            #b1h
            #print features
            #print len(features)
            WaveSmart_Feat.B1HM1= features[0]
            WaveSmart_Feat.B1HM2= features[1]
            WaveSmart_Feat.B1HM3= features[2]
            WaveSmart_Feat.B1HM4= features[3]
            WaveSmart_Feat.B1HM5= features[4]
            WaveSmart_Feat.B1HM6= features[5]
            WaveSmart_Feat.B1HM7= features[6]
            WaveSmart_Feat.B1HM8= features[7]
            WaveSmart_Feat.B1HM9= features[8]
            #b1v
            WaveSmart_Feat.B1HV1= features[9]
            WaveSmart_Feat.B1HV2= features[10]
            WaveSmart_Feat.B1HV3= features[11]
            WaveSmart_Feat.B1HV4= features[12]
            WaveSmart_Feat.B1HV5= features[13]
            WaveSmart_Feat.B1HV6= features[14]
            WaveSmart_Feat.B1HV7= features[15]
            WaveSmart_Feat.B1HV8= features[16]
            WaveSmart_Feat.B1HV9= features[17]
            #b1D
            WaveSmart_Feat.B1HD1= features[18]
            WaveSmart_Feat.B1HD2= features[19]
            WaveSmart_Feat.B1HD3= features[20]
            WaveSmart_Feat.B1HD4= features[21]
            WaveSmart_Feat.B1HD5= features[22]
            WaveSmart_Feat.B1HD6= features[23]
            WaveSmart_Feat.B1HD7= features[24]
            WaveSmart_Feat.B1HD8= features[25]
            WaveSmart_Feat.B1HD9= features[26]

            if (numberOfBands>=3):
                #b2h
                WaveSmart_Feat.B2HM1= features[27]
                WaveSmart_Feat.B2HM2= features[28]
                WaveSmart_Feat.B2HM3= features[29]
                WaveSmart_Feat.B2HM4= features[30]
                WaveSmart_Feat.B2HM5= features[31]
                WaveSmart_Feat.B2HM6= features[32]
                WaveSmart_Feat.B2HM7= features[33]
                WaveSmart_Feat.B2HM8= features[34]
                WaveSmart_Feat.B2HM9= features[35]
                #b2v
                WaveSmart_Feat.B2HV1= features[36]
                WaveSmart_Feat.B2HV2= features[37]
                WaveSmart_Feat.B2HV3= features[38]
                WaveSmart_Feat.B2HV4= features[39]
                WaveSmart_Feat.B2HV5= features[40]
                WaveSmart_Feat.B2HV6= features[41]
                WaveSmart_Feat.B2HV7= features[42]
                WaveSmart_Feat.B2HV8= features[43]
                WaveSmart_Feat.B2HV9= features[44]
                #b2D
                WaveSmart_Feat.B2HD1= features[45]
                WaveSmart_Feat.B2HD2= features[46]
                WaveSmart_Feat.B2HD3= features[47]
                WaveSmart_Feat.B2HD4= features[48]
                WaveSmart_Feat.B2HD5= features[49]
                WaveSmart_Feat.B2HD6= features[50]
                WaveSmart_Feat.B2HD7= features[51]
                WaveSmart_Feat.B2HD8= features[52]
                WaveSmart_Feat.B2HD9= features[53]

                #b3h
                WaveSmart_Feat.B3HM1= features[54]
                WaveSmart_Feat.B3HM2= features[55]
                WaveSmart_Feat.B3HM3= features[56]
                WaveSmart_Feat.B3HM4= features[57]
                WaveSmart_Feat.B3HM5= features[58]
                WaveSmart_Feat.B3HM6= features[59]
                WaveSmart_Feat.B3HM7= features[60]
                WaveSmart_Feat.B3HM8= features[61]
                WaveSmart_Feat.B3HM9= features[62]
                #b3v
                WaveSmart_Feat.B3HV1= features[63]
                WaveSmart_Feat.B3HV2= features[64]
                WaveSmart_Feat.B3HV3= features[65]
                WaveSmart_Feat.B3HV4= features[66]
                WaveSmart_Feat.B3HV5= features[67]
                WaveSmart_Feat.B3HV6= features[68]
                WaveSmart_Feat.B3HV7= features[69]
                WaveSmart_Feat.B3HV8= features[70]
                WaveSmart_Feat.B3HV9= features[71]
                #b3D
                WaveSmart_Feat.B3HD1= features[72]
                WaveSmart_Feat.B3HD2= features[73]
                WaveSmart_Feat.B3HD3= features[74]
                WaveSmart_Feat.B3HD4= features[75]
                WaveSmart_Feat.B3HD5= features[76]
                WaveSmart_Feat.B3HD6= features[77]
                WaveSmart_Feat.B3HD7= features[78]
                WaveSmart_Feat.B3HD8= features[79]
                WaveSmart_Feat.B3HD9= features[80]

            if (numberOfBands==4):
                #b4h
                WaveSmart_Feat.B4HM1= features[81]
                WaveSmart_Feat.B4HM2= features[82]
                WaveSmart_Feat.B4HM3= features[83]
                WaveSmart_Feat.B4HM4= features[84]
                WaveSmart_Feat.B4HM5= features[85]
                WaveSmart_Feat.B4HM6= features[86]
                WaveSmart_Feat.B4HM7= features[87]
                WaveSmart_Feat.B4HM8= features[88]
                WaveSmart_Feat.B4HM9= features[89]
                #b4v
                WaveSmart_Feat.B4HV1= features[90]
                WaveSmart_Feat.B4HV2= features[91]
                WaveSmart_Feat.B4HV3= features[92]
                WaveSmart_Feat.B4HV4= features[93]
                WaveSmart_Feat.B4HV5= features[94]
                WaveSmart_Feat.B4HV6= features[95]
                WaveSmart_Feat.B4HV7= features[96]
                WaveSmart_Feat.B4HV8= features[97]
                WaveSmart_Feat.B4HV9= features[98]
                #b4D
                WaveSmart_Feat.B4HD1= features[99]
                WaveSmart_Feat.B4HD2= features[100]
                WaveSmart_Feat.B4HD3= features[101]
                WaveSmart_Feat.B4HD4= features[102]
                WaveSmart_Feat.B4HD5= features[103]
                WaveSmart_Feat.B4HD6= features[104]
                WaveSmart_Feat.B4HD7= features[105]
                WaveSmart_Feat.B4HD8= features[106]
                WaveSmart_Feat.B4HD9= features[107]
            return WaveSmart_Feat
        except GenException, e:
            raise e

    def IQM_Features(self, image):
        try:
            IQM_Feat = IQMFeat.IQMFeat()
            imagenO = self.imageToMatriz(image)
            M,N = image.size
            imagenS = self.gaussianFilter(image, imagenO, 0.5, 1)

            IQM_Feat.minkowsky1 = funcionesC.minkowskyMetric(imagenO, imagenS, 1)
            IQM_Feat.minkowsky2 = funcionesC.minkowskyMetric(imagenO, imagenS, 2)
            IQM_Feat.normCrossCor = funcionesC.normalizedCrossCorrelation(imagenO, imagenS)
            IQM_Feat.structCont = funcionesC.structuralContent(imagenO, imagenS)
            hvs = self.hvsMeasures(imagenO, imagenS)
            IQM_Feat.hvsNormAbseErr = hvs[0:3]
            IQM_Feat.hvsBasedL2 = hvs[3:6]
            IQM_Feat.laplacianMSE = funcionesC.laplacianMeanSquareError(imagenO, imagenS)
            IQM_Feat.czekonowskyDist = funcionesC.czekonowskyDistance(imagenO, imagenS)

            mbf = self.medianBlockFeatures(imagenO, imagenS, 32, 2, 2.5*(10**-5))

            dftO = self.discreteFourierTransform(imagenO,N,M)
            dftS = self.discreteFourierTransform(imagenS,N,M)
            IQM_Feat.spectralPhase = funcionesC.spectralPhase(dftO, dftS)
            IQM_Feat.spectralMagnit = funcionesC.spectralMagnitude(dftO, dftS)
            dftO = None
            dftS = None
            IQM_Feat.wSpectralDist = self.weightedSpectralDistance(IQM_Feat.spectralPhase, IQM_Feat.spectralMagnit, 2.5*(10**-5))
            IQM_Feat.medianBlockSpecMag = mbf[0:3]
            IQM_Feat.medianBlockSpecPh = mbf[3:6]
            IQM_Feat.medianBlockWSpecDist = mbf[6:9]

            return IQM_Feat
        except GenException, e:
            raise e


    def proceso(self, q):
        try:
            salir = False
            while(not salir):
                imagePath = q.get()
                self.caracteristicas(imagePath)
                if(q.empty()):
                    salir = True
        except GenException, e:
            raise e

    def getAllFeaturesMultiprocess(self, imagePath):
        try:
            inicio = time.time()
            path = os.path.join(imagePath, "*.jpg")
            listaImagenes = glob.glob(path)
            q = multiprocessing.Queue()
            for i in range(len(listaImagenes)):
                q.put(listaImagenes[i])
            procesos = []
            i = 0
            while(i<multiprocessing.cpu_count() and i<len(listaImagenes)):
                p = multiprocessing.Process(target=self.proceso, args=(q,))
                procesos.append(p)
                p.start()
                i=i+1
            for i in range(len(procesos)):
                procesos[i].join()

            fin = time.time()
            tiempo_total = fin - inicio
            print "Tiempo total: " + str(tiempo_total) + " segundos"
        except GenException, e:
            raise e


if __name__ == '__main__':
    imF = imageFeatures()
    #imF.getAllFeatures("C:\Users\Sergio\Desktop\Fotos")
