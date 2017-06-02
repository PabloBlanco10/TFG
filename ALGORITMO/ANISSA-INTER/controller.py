from DB import dBInsert
import os
import configuration
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Controller:

    #Directorio donde se encuentran las muestras para analizar#
    def __init__(self, dirPath, outPath, fileType, Feat2Extract, Experimento,trainTest=True):
        """
        \param dirPath (string) Root path of all the pictures (models and brands)
        \param outPath (string) Path where the files of class and features will be create
        \param fileType (string) Type of image format, could be: jpg, jpeg, png, gif...etc.
        """
        self.dirPath = dirPath
        self.outPath = outPath
        self.fileType = fileType
        self.Feat2Extract = Feat2Extract
        self.trainTest = trainTest
        self.Experimento = Experimento

    def generateFileList(self):
        count = 0
        lstProject = []
        print self.dirPath
        for root, subdirs, files in os.walk(self.dirPath):
            if files.__len__()!=0:
                if root.__str__()[self.dirPath.__len__():].__len__() !=0:
                    lstFiles = []
                    for file in files:
                        if dBInsert.isImage(root,file):
                            lstFiles.append(file)
                    if lstFiles.__len__() > 0:
                        lstProject.append([count,root,files])
                        count +=1
                else:
                    lstFiles = []
                    for file in files:
                        if dBInsert.isImage(root,file):
                            lstFiles.append(file)
                    if lstFiles.__len__() > 0:
                        lstProject.append([count, root, lstFiles])
                        count += 1
        self.createFeaturesFile(lstProject)

    def createFeaturesFile(self,lstProject):
        for elements in lstProject:
            dBInsert.insertPhotosParalel(elements[2], 1, elements[1], self.outPath, self.Feat2Extract, self.Experimento,self.trainTest,"Y")


def main():
    #Lista de Caracteristicas - Para imprimirlos en la consola
    ###listFeat = ["Color","Wavelets", "IQM", "PRNU", "Todas"]
    #Lista de Extensiones - Para imprimirlos en la consola
    ###listExt = ["JPEG/JPG", "PNG", "Todas"]
    #Declaracion e inicializacion del Objeto Controller, para ejecutar despues el analisis.
    #####################Comunicacion con el usuario a traves de la consola.#####################
    ###print bcolors.HEADER + "Bienvenidos!!\nVamos a Configurar el sistema de analisis de imagenes\n"+bcolors.ENDC
    ###print bcolors.FAIL + "Donde se halla la imagen o el directorio contenedor de imagnes\ncoloca la direccion absoluta del directorio o fichero.\nEste script se esta ejecutando en la direccion:\n" +" "+bcolors.ENDC + bcolors.WARNING +str(os.getcwd())+ bcolors.ENDC
    ###pathAnalysis = raw_input("Escribe la direccion absoluta: ")
    if os.path.exists(configuration.FolderTrain):
        theia = Controller(configuration.FolderTrain, configuration.Results, "jpg", configuration.Features, configuration.Experimento)
        theia.generateFileList()
        if not os.path.exists(configuration.Results):
            os.makedirs(configuration.Results)
        fg = open(configuration.Results + os.sep + "experimentConstant.txt", "w")
        fg.write("Fecha de Experimento: " + str(time.strftime("%c")) + '\n')
        fg.write("Experimento: "+str(configuration.Experimento)+'\n')
        fg.write("Carpeta de Entrenamiento: " + str(configuration.FolderTrain) + '\n')
        fg.write("Carpeta de Prueba: " + str(configuration.FolderTest) + '\n')
        fg.write("Caracteristicas analizadas: " + str(configuration.Features) + '\n')

        dBInsert.filesGeneration(configuration.Results,configuration.Experimento)
        if os.path.exists(configuration.FolderTest):
            theiaTest = Controller(configuration.FolderTest, configuration.Results, "jpg", configuration.Features,configuration.Experimento, False)
            theiaTest.generateFileList()
            dBInsert.testSVMMongo(configuration.Results, configuration.Experimento)
    else:
        print bcolors.FAIL + "El directorio o fichero escrito no existe\n" + bcolors.ENDC
        main()

main()
