

from Exception.exception import GenException
from Features import imageFeaturesC
from PRNU.prnu import *
import multiprocessing
from multiprocessing import Lock
import time
from Features import ColorFeat
from Features import IQMFeat
from Features.ScanVsCamera_SVM import scanVsCamera
from PRNU import prnu
from Features.SVMClass import SVMClass
from LBP import Basic3x3LBP as LBP

##New Imports for Mongo Connection and EXIF extraction##
import EXIF2
from pymongo import MongoClient
import numpy as np
import hashlib
import itertools
#import json
#from bson import Binary, Code
#from bson.json_util import dumps, loads
client = MongoClient('localhost', 27017)
db = client.theiaTest
########################################################


def ColorFeatures(filename, idImage):
    try:
        InsColor_Feat = None
        imf = imageFeaturesC.imageFeatures()
        CF = ColorFeat.ColorFeat()
        if CROP_REQUIRED:
            img = cropImageFilename(filename, CROP_X_SIZE, CROP_Y_SIZE, CROPCENT_REQUIRED)
        else:
            img = Image.open(filename)
        mode = img.mode
        if (mode == "1" or mode == "L" or mode == "P" or mode == "I" or mode == "F" or  ##one band
                    mode == "RGB" or mode == "YCbCr" or  ##three bands
                    mode == "RGBA" or mode == "CMYK"):  ##four bands
            CF = imf.Color_Features(img)
            InsColor_Feat = "insert into Color_Features(IdImage,"
            valColor_Feat = []
            valColor_Feat = genInsFeature(InsColor_Feat, valColor_Feat, "avgPixVal", CF.averagePixelValue)
            valColor_Feat = genInsFeature(InsColor_Feat, valColor_Feat, "rgbPairsCor", CF.rgbPairsCorrelation)
            valColor_Feat = genInsFeature(InsColor_Feat, valColor_Feat, "DistCentMass", CF.rgbPairsEnergyRatio)
            valColor_Feat = genInsFeature(InsColor_Feat, valColor_Feat, "rgbEnergyRat", CF.rgbPairsEnergyRatio)
            #valColor_Feat = valColor_Feat[:len(valColor_Feat) - 1]

        return valColor_Feat

    except GenException, e:
        raise e

def WaveletsSmartFeatures(filename, idImage):
    try:
        imf = imageFeaturesC.imageFeatures()
        if CROP_REQUIRED:
            img = cropImageFilename(filename, CROP_X_SIZE, CROP_Y_SIZE, CROPCENT_REQUIRED)
        else:
            img = Image.open(filename)
        mode=img.mode
        if(mode == "1" or mode == "L"  or mode == "P" or mode == "I"  or mode == "F" or ##one band
           mode == "RGB" or mode == "YCbCr" or ##three bands
           mode == "RGBA" or mode == "CMYK"): ##four bands
            WF = imf.WaveletsSmart_Features(image2array(img))
            valWave_Feat =  [round(WF.B1HM1,20), round(WF.B1HM2,20), round(WF.B1HM3,20),
                             round(WF.B1HM4,20), round(WF.B1HM5,20), round(WF.B1HM6,20),
                             round(WF.B1HM7,20), round(WF.B1HM8,20), round(WF.B1HM9,20),
                             round(WF.B1HV1,20), round(WF.B1HV2,20), round(WF.B1HV3,20),
                             round(WF.B1HV4,20), round(WF.B1HV5,20), round(WF.B1HV6,20),
                             round(WF.B1HV7,20), round(WF.B1HV8,20), round(WF.B1HV9,20),
                             round(WF.B1HD1,20), round(WF.B1HD2,20), round(WF.B1HD3,20),
                             round(WF.B1HD4,20), round(WF.B1HD5,20), round(WF.B1HD6,20),
                             round(WF.B1HD7,20), round(WF.B1HD8,20), round(WF.B1HD9,20),
                             round(WF.B2HM1,20), round(WF.B2HM2,20), round(WF.B2HM3,20),
                             round(WF.B2HM4,20), round(WF.B2HM5,20), round(WF.B2HM6,20),
                             round(WF.B2HM7,20), round(WF.B2HM8,20), round(WF.B2HM9,20),
                             round(WF.B2HV1,20), round(WF.B2HV2,20), round(WF.B2HV3,20),
                             round(WF.B2HV4,20), round(WF.B2HV5,20), round(WF.B2HV6,20),
                             round(WF.B2HV7,20), round(WF.B2HV8,20), round(WF.B2HV9,20),
                             round(WF.B2HD1,20), round(WF.B2HD2,20), round(WF.B2HD3,20),
                             round(WF.B2HD4,20), round(WF.B2HD5,20), round(WF.B2HD6,20),
                             round(WF.B2HD7,20), round(WF.B2HD8,20), round(WF.B2HD9,20),
                             round(WF.B3HM1,20), round(WF.B3HM2,20), round(WF.B3HM3,20),
                             round(WF.B3HM4,20), round(WF.B3HM5,20), round(WF.B3HM6,20),
                             round(WF.B3HM7,20), round(WF.B3HM8,20), round(WF.B3HM9,20),
                             round(WF.B3HV1,20), round(WF.B3HV2,20), round(WF.B3HV3,20),
                             round(WF.B3HV4,20), round(WF.B3HV5,20), round(WF.B3HV6,20),
                             round(WF.B3HV7,20), round(WF.B3HV8,20), round(WF.B3HV9,20),
                             round(WF.B3HD1,20), round(WF.B3HD2,20), round(WF.B3HD3,20),
                             round(WF.B3HD4,20), round(WF.B3HD5,20), round(WF.B3HD6,20),
                             round(WF.B3HD7,20), round(WF.B3HD8,20), round(WF.B3HD9,20),
                             round(WF.B4HM1,20), round(WF.B4HM2,20), round(WF.B4HM3,20),
                             round(WF.B4HM4,20), round(WF.B4HM5,20), round(WF.B4HM6,20),
                             round(WF.B4HM7,20), round(WF.B4HM8,20), round(WF.B4HM9,20),
                             round(WF.B4HV1,20), round(WF.B4HV2,20), round(WF.B4HV3,20),
                             round(WF.B4HV4,20), round(WF.B4HV5,20), round(WF.B4HV6,20),
                             round(WF.B4HV7,20), round(WF.B4HV8,20), round(WF.B4HV9,20),
                             round(WF.B4HD1,20), round(WF.B4HD2,20), round(WF.B4HD3,20),
                             round(WF.B4HD4,20), round(WF.B4HD5,20), round(WF.B4HD6,20),
                             round(WF.B4HD7,20), round(WF.B4HD8,20), round(WF.B4HD9,20)]
        return valWave_Feat
    except GenException, e:
        raise e


def WaveletsLBP(imgCr, imgCb):
    try:
        imf = imageFeaturesC.imageFeatures()
        #if CROP_REQUIRED:
        #    img = cropImageFilename(filename, CROP_X_SIZE, CROP_Y_SIZE, CROPCENT_REQUIRED)
        #else:
        #    img = Image.open(filename)
        mode=imgCr.mode
        if(mode == "1" or mode == "L"  or mode == "P" or mode == "I"  or mode == "F" or ##one band
           mode == "RGB" or mode == "YCbCr" or ##three bands
           mode == "RGBA" or mode == "CMYK"): ##four bands
            WFCr = imf.WaveletsSmart_Features(image2array(imgCr))
            WFCb = imf.WaveletsSmart_Features(image2array(imgCb))
            valWave_Feat =  [round(WFCr.B1HM1,20), round(WFCr.B1HM2,20), round(WFCr.B1HM3,20),
                             round(WFCr.B1HM4,20), round(WFCr.B1HM5,20), round(WFCr.B1HM6,20),
                             round(WFCr.B1HM7,20), round(WFCr.B1HM8,20), round(WFCr.B1HM9,20),
                             round(WFCr.B1HV1,20), round(WFCr.B1HV2,20), round(WFCr.B1HV3,20),
                             round(WFCr.B1HV4,20), round(WFCr.B1HV5,20), round(WFCr.B1HV6,20),
                             round(WFCr.B1HV7,20), round(WFCr.B1HV8,20), round(WFCr.B1HV9,20),
                             round(WFCr.B1HD1,20), round(WFCr.B1HD2,20), round(WFCr.B1HD3,20),
                             round(WFCr.B1HD4,20), round(WFCr.B1HD5,20), round(WFCr.B1HD6,20),
                             round(WFCr.B1HD7,20), round(WFCr.B1HD8,20), round(WFCr.B1HD9,20),
                             round(WFCb.B1HM1, 20), round(WFCb.B1HM2, 20), round(WFCb.B1HM3, 20),
                             round(WFCb.B1HM4, 20), round(WFCb.B1HM5, 20), round(WFCb.B1HM6, 20),
                             round(WFCb.B1HM7, 20), round(WFCb.B1HM8, 20), round(WFCb.B1HM9, 20),
                             round(WFCb.B1HV1, 20), round(WFCb.B1HV2, 20), round(WFCb.B1HV3, 20),
                             round(WFCb.B1HV4, 20), round(WFCb.B1HV5, 20), round(WFCb.B1HV6, 20),
                             round(WFCb.B1HV7, 20), round(WFCb.B1HV8, 20), round(WFCb.B1HV9, 20),
                             round(WFCb.B1HD1, 20), round(WFCb.B1HD2, 20), round(WFCb.B1HD3, 20),
                             round(WFCb.B1HD4, 20), round(WFCb.B1HD5, 20), round(WFCb.B1HD6, 20),
                             round(WFCb.B1HD7, 20), round(WFCb.B1HD8, 20), round(WFCb.B1HD9, 20)]
        return valWave_Feat
    except GenException, e:
        raise e


def IQMFeatures(filename,idImage):
    try:

        imf = imageFeaturesC.imageFeatures()
        IQMF = IQMFeat.IQMFeat()
        if CROP_REQUIRED:
            img = cropImageFilename(filename, CROP_X_SIZE, CROP_Y_SIZE, CROPCENT_REQUIRED)
        else:
            img = Image.open(filename)
        InsIQM_Feat = None
        mode=img.mode
        if(mode == "1" or mode == "L"  or mode == "P" or mode == "I"  or mode == "F" or ##one band
           mode == "RGB" or mode == "YCbCr" or ##three bands
           mode == "RGBA" or mode == "CMYK"): ##four bands
            IQMF = imf.IQM_Features(img)
            InsIQM_Feat = "insert into IQM_Features(IdImage,"
            valIQM_Feat = []
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "minkowsky1", IQMF.minkowsky1)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "minkowsky2",IQMF.minkowsky2)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "normCrossCor", IQMF.normCrossCor)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "structCont", IQMF.structCont)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "hvsNormAbseErr", IQMF.hvsNormAbseErr)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "hvsBasedL2",IQMF.hvsBasedL2)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "laplacianMSE", IQMF.laplacianMSE)
            valIQM_Feat.append(round(IQMF.czekonowskyDist,20))
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "spectralPhase", IQMF.spectralPhase)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "spectralMagnit", IQMF.spectralMagnit)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "wSpectralDist",IQMF.wSpectralDist)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "medianBlockSpecMag", IQMF.medianBlockSpecMag)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "medianBlockSpecPh", IQMF.medianBlockSpecPh)
            valIQM_Feat= genInsFeature(InsIQM_Feat, valIQM_Feat, "medianBlockWSpecDist", IQMF.medianBlockWSpecDist)
            #valIQM_Feat = valIQM_Feat[:len(valIQM_Feat) - 1]
        return valIQM_Feat##InsIQM_Feat

    except GenException, e:
        raise e

def NoiseFeatures(filename,idImage):
    try:

        if CROP_REQUIRED:
            img = cropImageFilename(filename, CROP_X_SIZE, CROP_Y_SIZE, CROPCENT_REQUIRED)
        else:
            img = Image.open(filename)
        InsNoise_Feat = None
        mode=img.mode
        if(mode == "1" or mode == "L"  or mode == "P" or mode == "I"  or mode == "F" or ##one band
           mode == "RGB" or mode == "YCbCr" or ##three bands
           mode == "RGBA" or mode == "CMYK"): ##four bands
            classSvsC = scanVsCamera(img)
            valNoise_Feat = [round(classSvsC.mediaCol,20),round(classSvsC.mediaRow,20),round(classSvsC.medianaCol,20),
                  round(classSvsC.medianaRow,20),round(classSvsC.maxCol,20),round(classSvsC.maxRow,20),
                  round(classSvsC.minCol,20),round(classSvsC.minRow,20),round(classSvsC.varianzaCol,20),
                  round(classSvsC.varianzaRow,20),round(classSvsC.kurtosisCol,20),round(classSvsC.kurtosisRow,20),
                  round(classSvsC.skewnessCol,20),round(classSvsC.skewnessRow,20),round(classSvsC.ratio,20),
                  round(classSvsC.mediaNoise,20)]
            valNoise_Feat = changeNAN2Zero(valNoise_Feat)
        return valNoise_Feat

    except GenException, e:
        raise e

def extractFeatures(q,lock,IdProject,idProc,pathFile, FeatureExtract, outFile, Feat2Extract, Experimento,trainTest):
    if(q.empty()):
        salir = True
    else:
        salir = False
    while(not salir):
        filename = q.get()
        IdImage = checkSumFileID(pathFile+"/" +filename)
        exist = alreadyExist(pathFile,IdImage, trainTest)
        ClassType = pathFile.split(os.sep)
        ClassType = ClassType[ClassType.__len__() - 1]
        fileBin = open(pathFile + "/" + filename, 'rb', 1)  # leer archivo para sacar
        fileBin.seek(0)
        #tags, errors = EXIF2.process_file(fileBin, detecErr=True)  # ,debug=True)#,details=True)#
        tags, errors = None,None

        #InsMain_info, InsImage_info, InsExif_info, InsGPS_info, InsInter_info, InsTHUMBNAIL_info, swMakerNote, binMaker, swBLOB, binThumb, InsJPEGThumbnail_info, valJPEGThumbnail_info = findTags(tags, errors, IdImage, filename, pathFile, IdProject)
        #print InsMain_info, InsImage_info, InsExif_info, InsGPS_info, InsInter_info, InsTHUMBNAIL_info, swMakerNote, binMaker, swBLOB, binThumb, InsJPEGThumbnail_info, valJPEGThumbnail_info

        document = documentCreation(IdImage, exist, pathFile, filename, tags, errors, ClassType, Experimento, trainTest)

        InsColor_Feat=[]
        InsWave_Feat=[]
        InsIQM_Feat=[]
        InsNoise_Feat=[]
        InsWaveLBP = []
        if (FeatureExtract=='Y'):

            if (Feat2Extract == 'WaveletsLBP' and document["LBP"] .__len__() == 0):
                imgCr,imgCb = LBP.lbp_cb_cr(pathFile+"/" +filename)
                InsWaveLBP = WaveletsLBP(imgCr,imgCb)#Modifica la funcion wavelets para trabajar con la matriz de la imagen
            if (Feat2Extract == 'Color' and document["ColorFeat"].__len__() == 0):
                InsColor_Feat = ColorFeatures(pathFile+"/" +filename, IdImage)
            if (Feat2Extract == 'Wavelets' and document["WaveletsFeat"] .__len__() == 0):
                InsWave_Feat = WaveletsSmartFeatures(pathFile+"/" +filename, IdImage)#Modifica la funcion wavelets para trabajar con la matriz de la imagen
            if (Feat2Extract == 'IQM' and document["IQMFeat"].__len__() == 0):
                InsIQM_Feat = IQMFeatures(pathFile+"/" +filename, IdImage)
            if (Feat2Extract == 'PRNU' and document["PRNU"].__len__() == 0):
                #InsNoise_Feat = NoiseFeatures(pathFile+"/" +filename, IdImage)
                noiseData = prnu.getNoise(pathFile, filename, True, WAVELET, LEVEL, MODE)  # para una imagen
                InsNoise_Feat = prnu.extractFeatures(noiseData, pathFile)
                #prnu.array2image(noiseData, 'RGB').save(pathFile + os.sep + NOISE_PREFIX + filename)
            if (Feat2Extract == 'Todas'):
                if document["ColorFeat"].__len__() == 0:
                    InsColor_Feat = ColorFeatures(pathFile + "/" + filename, IdImage)
                if document["WaveletsFeat"].__len__() == 0:
                    InsWave_Feat = WaveletsSmartFeatures(pathFile + "/" + filename, IdImage)
                if document["IQMFeat"].__len__() == 0:
                    InsIQM_Feat = IQMFeatures(pathFile + "/" + filename, IdImage)
                ##if document["PRNU"].__len__() == 0:
                    #InsNoise_Feat = NoiseFeatures(pathFile + "/" + filename, IdImage)
                ##    noiseData = prnu.getNoise(pathFile, filename, True, WAVELET, LEVEL, MODE)  # para una imagen
                ##    InsNoise_Feat = prnu.extractFeatures(noiseData, pathFile)
            insertImage2Mongo(InsColor_Feat, InsWave_Feat, InsIQM_Feat, InsNoise_Feat, InsWaveLBP, exist, document, Experimento, trainTest)
        else:
            insertImage2Mongo(InsColor_Feat, InsWave_Feat, InsIQM_Feat, InsNoise_Feat, InsWaveLBP, exist, document, Experimento, trainTest)
        lock.acquire()
        lock.release()
        if(q.empty()):
            salir = True

def isImage(pathFile, filename):
    """
    \brief Method that Opens and identifies the given image file.
    \param self (dBInsert::DBInsert).
    \param pathFile (string) Path of file.
    \param filename (string) Filename of image to open.
    \return swisImg (bool) swisImg = True when file is a image, swisImg = False when file isn't a image.
    \exception when file isn't a image will be insert a new item in the list (lstError) with information that indicate the error.
    """
    try:
        filename=os.path.join(pathFile, filename)
        swisImg = False
        i=Image.open(filename)
        swisImg = True
    except IOError, e:
        strError = "Filename: %s, Path: %s %s" % (filename, pathFile, e)
        print strError
    return swisImg

def genInsFeature(InsSQLFeat, valSQLFeat, nameFeat, valFeat):
    try:
            InsSQLFeat += nameFeat+"R," + nameFeat+"G," + nameFeat+"B,"
            valSQLFeat += [round(valFeat[0],20), round(valFeat[1],20), round(valFeat[2],20)]
            #valSQLFeat += "%s,%s,%s,"% (round(valFeat[0],20), round(valFeat[1],20), round(valFeat[2],20))
            return valSQLFeat
    except GenException, e:
        raise e
#-- DBInsert.insertPhotos



def insertPhotosParalel(lstFiles, IdProject, pathFile, outFile, Feat2Extract, Experimento, trainTest, FeatureExtract='N'):
    """
    \brief Method that to open file that have data to insert in database.
    \brief In this method it called a insertTags Method for to insert new image in Database.
    \param self (dBInsert::DBInsert).
    \param lstFiles (list) list files to insert.
    \param IdProject (int) Project identification.
    \param pathFile (string) Path of file.
    \return No return.
    """
    try:
        start = time.time()
        #"Insertar fotos"
        q = multiprocessing.Queue()
        ## q es una cola donde se mete la lista de archivos
        for i in range(len(lstFiles)):
            swInsert=False
            name_file=lstFiles[i]
            swInsert=isImage(pathFile, name_file)
            if swInsert== True:
                q.put(lstFiles[i])
        procesos = []
        idProc = 0
        lock = Lock()
        #print multiprocessing.cpu_count()
        while(idProc<multiprocessing.cpu_count() and idProc<len(lstFiles)):
            p = multiprocessing.Process(target=extractFeatures(q,lock,IdProject,idProc,pathFile,FeatureExtract,outFile, Feat2Extract, Experimento, trainTest))
            procesos.append(p)
            p.start()
            idProc=idProc+1

        for idProc in range(len(procesos)):
            procesos[idProc].join()

        print "Tiempo trascurrido: " +  str(time.time()-start)

    except GenException, e:
        raise e
#-- DBInsert.insertPhotos }


def getFiles(nameDir,typeFile):
    """
    #typeFile =['jpeg','jpg','png', 'gif']
    \brief Method that gets list files in a Path.
    \param self (dBInsert::DBInsert).
    \param nameDir (string) Path.
    \param typeFile (string) Type Files to search.
    \return lstFiles (list) list found files in path.
    """
    try:
        os.chdir(nameDir)
        typeFile = "*." + typeFile
        lstFiles = glob.glob(typeFile)
        return lstFiles
    except GenException, e:
        raise e
#-- DBInsert.getFiles }


def insertImage2Mongo(InsColor_Feat, InsWave_Feat, InsIQM_Feat, InsNoise_Feat, InsWaveLBP, exist, document, Experimento, trainTest):
    if trainTest:
        mongoDB = db.Fotos
    else:
        mongoDB = db.FotosTest

    if exist:
        if InsColor_Feat.__len__() > 0:
            document["ColorFeat"] = InsColor_Feat
            document["ExtractedFeatures"] = document["ExtractedFeatures"] + InsColor_Feat
        if InsWave_Feat.__len__() > 0:
            document["WaveletsFeat"] = InsWave_Feat
            document["ExtractedFeatures"] = document["ExtractedFeatures"] + InsWave_Feat
        if InsIQM_Feat.__len__() > 0:
            document["IQMFeat"] =  InsIQM_Feat
            document["ExtractedFeatures"] = document["ExtractedFeatures"] + InsIQM_Feat
        if InsNoise_Feat.__len__() > 0:
            document["PRNU"] = InsNoise_Feat
            document["ExtractedFeatures"] = document["ExtractedFeatures"] + InsNoise_Feat
        if InsWaveLBP.__len__() > 0:
            document["LBP"] = InsWaveLBP
            document["ExtractedFeatures"] = document["ExtractedFeatures"] + InsWaveLBP
        mongoDB.update(
        {"$and":[{"Path":str(document["Path"])},{"IdImage":str(document["IdImage"])}]},
        {
            "Path": str(document["Path"]),
            #"Class": document["Class"],
            "IdImage": document["IdImage"],
            "ColorFeat": document["ColorFeat"],
            "WaveletsFeat": document["WaveletsFeat"],
            "IQMFeat": document["IQMFeat"],
            "LBP": document["LBP"],
            "PRNU": document["PRNU"],
            "File": str(document["File"]),
            "TagsExif": document["TagsExif"],
            "ErrorTags": document["ErrorTags"],
            "ClassType": document["ClassType"],
            "ExtractedFeatures": document["ExtractedFeatures"],
            "Experimento": document["Experimento"],
        },
        True
        )
    else:
        document["ColorFeat"]= InsColor_Feat
        document["WaveletsFeat"] = InsWave_Feat
        document["IQMFeat"] =  InsIQM_Feat
        document["PRNU"] = InsNoise_Feat
        document["LBP"] = InsWaveLBP
        document["ExtractedFeatures"] = InsColor_Feat+InsWave_Feat+InsIQM_Feat+InsNoise_Feat+InsWaveLBP
        document["Experimento"] = Experimento
        mongoDB.insert_one(document)



'''
def createClassFile(listFeatures,outFile,classSVM):
    indice = 0
    f = open(outFile+"imagesFeatures.train", "a")
    f.write(str(classSVM) + " ")
    for features in listFeatures:
        f.write(str(indice)+":"+str(features)+" ")
        indice+=1
    f.write("\n")
    f.close()
'''


def newPRNUFeatureExtrct():
    #getNoise()
    extractFeatures()

def changeNAN2Zero(listOrarray):
    array2return = []
    for element in listOrarray:
        if np.isnan(element) or np.isinf(element):
            array2return.append(0.0)
        else:
            array2return.append(element)
    return array2return

def checkSumFileID(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def alreadyExist(path,IdImage,trainTest):
    if trainTest:
        if db.Fotos.find({"IdImage": IdImage}).count() > 0:  # (db.Fotos.find({"IdImage": IdImage}).count() > 0):
            return True
        else:
            return False
    else:
        if db.FotosTest.find({"IdImage": IdImage}).count() > 0:  # (db.Fotos.find({"IdImage": IdImage}).count() > 0):
            return True
        else:
            return False

def isTheSame(path,IdImage,trainTest):
    if trainTest:
        if db.Fotos.find({"$and":[{"Path":str(path)}, {"IdImage":IdImage}]}).count() > 0:#(db.Fotos.find({"IdImage": IdImage}).count() > 0):
            return True
        else:
            return False
    else:
        if db.FotosTest.find({"$and":[{"Path":str(path)}, {"IdImage":IdImage}]}).count() > 0:#(db.Fotos.find({"IdImage": IdImage}).count() > 0):
            return True
        else:
            return False

def documentCreation(IdImage, exist, path, filename, tagsExif, errorTags, ClassType, Experimento, trainTest):
    same = isTheSame(path,IdImage,trainTest)
    if exist and same:
        if trainTest:
            document = db.Fotos.find_one({"$and":[{"Path":str(path)}, {"IdImage":IdImage}]})
            return document
        else:
            document = db.FotosTest.find_one({"$and": [{"Path": str(path)}, {"IdImage": IdImage}]})
            return document
    elif exist:
        if trainTest:
            document = db.Fotos.find_one({"IdImage":IdImage})
        else:
            document = db.FotosTest.find_one({"IdImage": IdImage})
        document["Path"] = str(path)
        #document["Class"] = classSVM
        document["File"] = filename
        document["TagsExif"] = None#tagsExif#Dictionary of Tags EXIF
        document["ErrorTags"] = None#errorTags#Dictionary of Error in Tags of EXIF
        document["ClassType"] = ClassType
        document["Experimento"] = Experimento
        return document
    else:
        document = {
                "Path": path,
                #"Class": classSVM,
                "IdImage": IdImage,
                "ColorFeat": [],
                "WaveletsFeat": [],
                "IQMFeat": [],
                "PRNU": [],
                "LBP": [],
                "File": filename,
                "TagsExif": None,#tagsExif,
                "ErrorTags": None,#errorTags
                "ClassType": ClassType,
                "ExtractedFeatures": None,
                "Experimento": Experimento
                }
        return document

def findTags(tags, errors, idImage, fileName, PathOrigen, IdPrj):
    """
    \brief Method that insert new image in Database.
    \param self (dBInsert::DBInsert).
    \param tags (dictionary) Dictionary of main EXIF tag names.
    \param idImage (string) Image identification.
    \param fileName (string) Filename of image to insert in main_info table.
    \param PathOrigen (string) Path of file.
    \param IdPrj (int) Project identification.
    \exception If there is any error in image insertion will be create a list (lstError) with information that indicate the error.
    \return swIns (bool) Indicates whether the insertion was successful.
    """
    try:
        exif_info = 'N'
        image_info = 'N'
        gps_info = 'N'
        interop_info = 'N'
        thumb_info = 'N'
        Maker_Note = 'N'
        binThumb = None
        binMaker = None
        exif_error = 'N'
        image_error = 'N'
        gps_error = 'N'
        interop_error = 'N'
        thumb_error = 'N'
        #swIns = False
        #idImage = str(idImg)
        IdProject = str(IdPrj)
        nFile, typeFile = os.path.splitext(fileName)
        typeFile = typeFile[1:len(typeFile)]

        InsImage_info = "insert into image_info(IdImage,"
        InsExif_info = "insert into exif_info(IdImage,"
        InsGPS_info = "insert into gps_info(IdImage,"
        InsInter_info = "insert into interoperability_info(IdImage,"
        InsJPEGThumbnail_info = "insert into jpegthumbnail_info(IdImage,"
        InsTHUMBNAIL_info = "insert into thumbnail_info(IdImage,"
        swBLOB = False
        swMakerNote = False

        valImage_info = "values('" + idImage + "',"
        valExif_info = "values('" + idImage + "',"
        valGPS_info = "values('" + idImage + "',"
        valInter_info = "values('" + idImage + "',"
        valJPEGThumbnail_info = "values('" + idImage + "',"
        valTHUMBNAIL_info = "values('" + idImage + "',"

        #for tag in tags.keys():
        #    #print (tags[tag])
        #    dat_tag="%s" % tag
        #    dat_tag = dat_tag.replace(" ","_")
        #    pos= dat_tag.find("_") #Busca el "_" para identificar la tabla
        #    campo = dat_tag[pos+1:]

        for tag in tags.keys():
            idTagVal=tags.get(tag)
            if tag == 'JPEGThumbnail':
                    #(InsJPEGThumbnail_info, valJPEGThumbnail_info)=self.setString('jpegthumbnail_info',InsJPEGThumbnail_info,campo,valJPEGThumbnail_info,tags[tag])
                    swBLOB=False
                    binThumb = idTagVal
                    swBLOB = True
            else:
                for campo in idTagVal.keys():

                    if tag == 'EXIF Interoperability':
                        interop_info = 'Y'
                        print campo
                        print idTagVal.get(campo)
                        #(InsInter_info, valInter_info)=self.setString('Interoperability_info',InsInter_info,campo,valInter_info,idTagVal.get(campo))
                    elif tag == 'EXIF':
                        exif_info = 'Y'
                        #(InsExif_info, valExif_info)=self.setString('exif_info',InsExif_info,campo,valExif_info,idTagVal.get(campo))
                        if campo == 'MakerNote' and swMakerNote == False:
                            binMaker = idTagVal.get(campo)
                            swMakerNote = True
                            Maker_Note = 'Y'
                    elif tag == 'Image':
                        image_info = 'Y'
                        #(InsImage_info, valImage_info)=self.setString('image_info',InsImage_info,campo,valImage_info,idTagVal.get(campo))
                    elif tag == 'GPS':
                        gps_info = 'Y'
                        #(InsGPS_info, valGPS_info)=self.setString('gps_info',InsGPS_info,campo,valGPS_info,idTagVal.get(campo))
                    elif tag == 'Thumbnail':
                        thumb_info = 'Y'
                        #(InsTHUMBNAIL_info, valTHUMBNAIL_info)=self.setString('thumbnail_info',InsTHUMBNAIL_info,campo,valTHUMBNAIL_info,idTagVal.get(campo))

        for tagError in errors.keys():
            if tagError == 'EXIF Interoperability':
                interop_error = 'Y'
            elif tagError == 'EXIF':
                exif_error = 'Y'
            elif tagError == 'Image':
                image_error = 'Y'
            elif tagError == 'GPS':
                gps_error = 'Y'
            elif tagError == 'Thumbnail':
                thumb_error = 'Y'

        InsImage_info = InsImage_info[:len(InsImage_info) - 1] + ")"
        InsExif_info = InsExif_info[:len(InsExif_info) - 1] + ")"

        InsInter_info = InsInter_info[:len(InsInter_info) - 1] + ")"
        InsGPS_info = InsGPS_info[:len(InsGPS_info) - 1] + ")"
        InsTHUMBNAIL_info = InsTHUMBNAIL_info[:len(InsTHUMBNAIL_info) - 1] + ")"

        valImage_info = valImage_info[:len(valImage_info) - 1] + ")"
        valExif_info = valExif_info[:len(valExif_info) - 1] + ")"
        valInter_info = valInter_info[:len(valInter_info) - 1] + ")"
        valGPS_info = valGPS_info[:len(valGPS_info) - 1] + ")"
        valTHUMBNAIL_info = valTHUMBNAIL_info[:len(valTHUMBNAIL_info) - 1] + ")"


        InsImage_info = InsImage_info + " " + valImage_info + ";"
        InsExif_info = InsExif_info + " " + valExif_info + ";"
        InsInter_info = InsInter_info + " " + valInter_info + ";"
        InsGPS_info = InsGPS_info + " " + valGPS_info + ";"
        InsTHUMBNAIL_info = InsTHUMBNAIL_info + " " + valTHUMBNAIL_info + ";"

        InsMain_info = "insert into main_info(IdImage, Filename, "\
                       " PathOrigen, typeFile, IdProject, exif_info, image_info,"  \
                       " gps_info, interop_info, thumb_info, maker_note, exif_error, image_error,"  \
                       " gps_error, interop_error, thumb_error)"
        InsMain_info = InsMain_info + " values('" + idImage + "','" + fileName + "','"+ PathOrigen +"','" + \
                       typeFile + "'," + IdProject + ",'" + exif_info + "','" + image_info + \
                        "','" + gps_info + "','" + interop_info + "','" + thumb_info + "','" + \
                        Maker_Note + "','" + exif_error + "','" + image_error + \
                        "','" + gps_error + "','" + interop_error + "','" + thumb_error + "')"

        #Gen Thumbnail
        #InsDiff, sqlUPjpgThum_info, fileBinData = self.createThumbnail(idImage, PathOrigen, fileName, binThumb, swBLOB,fileBin)
        #return InsMain_info, InsImage_info, InsExif_info, InsGPS_info, InsInter_info, InsTHUMBNAIL_info, swMakerNote, binMaker, swBLOB,  binThumb, InsJPEGThumbnail_info, valJPEGThumbnail_info, InsDiff, sqlUPjpgThum_info, fileBinData
        print InsMain_info
        return InsMain_info, InsImage_info, InsExif_info, InsGPS_info, InsInter_info, InsTHUMBNAIL_info, swMakerNote, binMaker, swBLOB,  binThumb, InsJPEGThumbnail_info, valJPEGThumbnail_info#, InsDiff, sqlUPjpgThum_info, fileBinData

    except GenException, e:
        raise e

def filesGeneration(outPath,Experiment):
    f = open(outPath+os.sep+"classRelation.clre", "w")
    g = open(outPath + os.sep + "imagesFeatures.train", "w")
    mongoPics = db.Fotos.find({'Experimento':Experiment})
    listClass = db.Fotos.distinct("ClassType", {'Experimento': Experiment})#db.Fotos.distinct("ClassType")
    for pic in mongoPics:
        #listClass.append([str(pic["Class"]) + " " + str(pic["ClassType"])])
        index = 0
        g.write(str(listClass.index(str(pic["ClassType"]))) + " ")
        listFeatures = pic["ExtractedFeatures"]
        for feat in listFeatures:
            g.write(str(index) + ":" + str(feat) + " ")
            index += 1
        g.write("\n")
    #listClass = np.unique(listClass)
    for element in listClass:
        f.write(str(listClass.index(str(element)))+" "+str(element) + "\n")
    f.close()
    g.close()
    moduleDic = {}
    classNum = 0
    for classItem in listClass:
        moduleDic[str(classItem)] = classNum
        classNum += 1
    fg = open(outPath + os.sep + "experimentConstant.txt", "a")
    if CROP_REQUIRED:
        fg.write("Se utilizo un recorte en todas las imagenes de: " +str(CROP_X_SIZE)+'x'+str(CROP_Y_SIZE) + '\n')
    else:
        fg.write("No se utilizo ningun recorte en las imagenes."+'\n'+" Todas fueron analizadas en su tamanio original")
    SVMC = SVMClass(outPath, "imagesFeatures.train", "classRelation.clre", moduleDic, "imagesFeatures_train.scale", "imagesFeatures_train.model", "imagesFeatures_train.range", "imagesFeatures.test", "imagesFeatures_test.predict", "imagesFeatures_test.scale")
    SVMC.trainSVM(outPath)

def testSVMMongo(outPath, Experiment):
    g = open(outPath + os.sep + "imagesFeatures.test", "w")
    mongoPics = db.FotosTest.find({'Experimento':Experiment})
    listClass = db.FotosTest.distinct("ClassType", {'Experimento': Experiment})  # db.Fotos.distinct("ClassType")
    for pic in mongoPics:
        index = 0
        g.write(str(listClass.index(str(pic["ClassType"]))) + " ")
        listFeatures = pic["ExtractedFeatures"]
        for feat in listFeatures:
            g.write(str(index) + ":" + str(feat) + " ")
            index += 1
        g.write("\n")
    g.close()
    moduleDic = {}
    for classItem in listClass:
        moduleDic[str(classItem)] = listClass.index(str(classItem))
    SVMC = SVMClass(outPath, "imagesFeatures.train", "classRelation.clre", moduleDic, "imagesFeatures_train.scale", "imagesFeatures_train.model", "imagesFeatures_train.range", "imagesFeatures.test", "imagesFeatures_test.predict", "imagesFeatures_test.scale")
    SVMC.testSVM(outPath,"imagesFeatures.train","imagesFeatures.test", "imagesFeatures_train.model", "imagesFeatures_train.range")


