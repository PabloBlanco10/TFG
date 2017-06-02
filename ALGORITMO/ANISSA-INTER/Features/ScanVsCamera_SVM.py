
import sys
sys.path.append("./")
from noise import statisticalValuesC

class scanVsCamera:

    #Path del archivo

    filePath = ""

    #Caracteristicas de primer orden

    mediaCol = 0.0
    medianaCol = 0.0
    maxCol = 0.0
    minCol = 0.0

    mediaRow = 0.0
    medianaRow = 0.0
    maxRow = 0.0
    minRow = 0.0

    #Caracterisitcas de alto orden

    varianzaCol = 0.0
    kurtosisCol = 0.0
    skewnessCol = 0.0

    varianzaRow = 0.0
    kurtosisRow = 0.0
    skewnessRow = 0.0

    ratio = 0.0

    #Caracteristica nueva

    mediaNoise = 0.0

    #Constructor por defecto

    def __init__(self,img):
        #filePath = fp
        self.extractToClass(img)

    #Funciona para extraer del organizar las caracteristicas

    def extractToClass(self,img):
        #self.filePath = filePath  
        lf = statisticalValuesC(img) #### para el insert

        self.mediaCol = lf[0]
        self.medianaCol = lf[1]
        self.maxCol = lf[2]
        self.minCol = lf[3]

        self.mediaRow = lf[7]
        self.medianaRow = lf[8]
        self.maxRow = lf[9]
        self.minRow = lf[10]

        self.varianzaCol = lf[4]
        self.kurtosisCol = lf[5]
        self.skewnessCol = lf[6]

        self.varianzaRow = lf[11]
        self.kurtosisRow = lf[12]
        self.skewnessRow = lf[13]

        self.ratio = lf[14]

        self.mediaNoise = lf[15]

    #Devuelve una lista de tuplas (Nombre caracteristica, valor) de las caracteristicas de primer orden.
    #Ejemplo [("Media columnas", 2,34545433),("Media filas", 2,78866544),...]
    def getCaracteristicasPrimerOrden(self):
        lpo = []
        lpo.append(("Media columnas",self.mediaCol))
        lpo.append(("Media filas",self.mediaRow))
        lpo.append(("Mediana columnas",self.medianaCol))
        lpo.append(("Mediana filas",self.medianaRow))
        lpo.append(("Maximo columnas",self.maxCol))
        lpo.append(("Maximo filas",self.maxRow))
        lpo.append(("Minimo columnas",self.minCol))
        lpo.append(("Minimo filas",self.minRow))

        return lpo

    #Devuelve una lista de tuplas (Nombre caracteristica, valor) de las caracteristicas de alto orden.
    #Ejemplo [("Varianza columnas", 2,34545433),("Varianza filas", 2,78866544),...]
    def getCaracteristicasAltoOrden(self):
        lao = []
        lao.append(("Varianza columnas",self.varianzaCol))
        lao.append(("Varianza filas",self.varianzaRow))
        lao.append(("Kurtosis columnas",self.kurtosisCol))
        lao.append(("Kurtosis filas",self.kurtosisRow))
        lao.append(("Skewness columnas",self.skewnessCol))
        lao.append(("Skewness filas",self.skewnessRow))
        lao.append(("Ratio (Media filas/Media columnas)",self.ratio))

        return lao

    #Devuelve la caracteristica Ruido Medio que no esta en ninguno de los grupos anteriores
    def getCaracteristicaRuidoMedio(self):
        return ("Ruido medio",self.mediaNoise)

    def getTodasCaracteristicas(self):
        return self.getCaracteristicasPrimerOrden() + self.getCaracteristicasAltoOrden() + [self.getCaracteristicaRuidoMedio()]


#Test
if __name__ == '__main__':

    classSvsC = scanVsCamera(sys.argv[1])

    print "Caracterisiticas de primer orden:\n"
    
    
    print classSvsC.getCaracteristicasPrimerOrden()
    print ""

    print "Caracterisiticas de alto orden:\n"
    print classSvsC.getCaracteristicasAltoOrden()
    print ""

    print "Caracterisitica ruido medio:\n"
    print classSvsC.getCaracteristicaRuidoMedio()
    print ""

    print "Totas las caracteristicas:\n"
    print classSvsC.getTodasCaracteristicas()
    print ""