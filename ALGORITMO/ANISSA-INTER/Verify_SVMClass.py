
def trainSVM(self, file_name=None):
    try:
        if(file_name==None):
            PathClass = self.PathClass
            FileClass = self.FileClass
            FileScale = self.FileScale
            FileModel = self.FileModel
            FileRange = self.FileRange
            file_name = os.path.join(PathClass, FileClass)
            scaled_file = os.path.join(PathClass, FileScale)
            model_file = os.path.join(PathClass, FileModel)
            range_file = os.path.join(PathClass, FileRange)
        # Pongo como ruta la del archivo actual para encontrar los archivos SVM
        print (os.path.dirname(os.path.abspath(__file__)))
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Definicion de ejecutables
        is_win32 = (sys.platform == 'win32')
        if not is_win32:
            svmscale_exe = "../LIBSVM/svm-scale"
            svmtrain_exe = "../LIBSVM/svm-train"
            svmpredict_exe = "../LIBSVM/svm-predict"
            grid_py = "../LIBSVM/grid.py"
            gnuplot_exe = "/usr/local/bin/gnuplot"
        else:
            # windows
            svmscale_exe = r"..\LIBSVM\svm-scale.exe"
            svmtrain_exe = r"..\LIBSVM\svm-train.exe"
            svmpredict_exe = r"..\LIBSVM\svm-predict.exe"
            grid_py = r"..\LIBSVM\grid.py"


        assert os.path.exists(svmscale_exe),"ERROR:svm-scale executable not found"
        assert os.path.exists(svmtrain_exe),"ERROR: svm-train executable not found"
        assert os.path.exists(svmpredict_exe),"ERROR:svm-predict executable not found"
        assert os.path.exists(grid_py),"ERROR:grid.py not found"

        #escalar datos
        cmd = '%s -s "%s" "%s" > "%s"' % (svmscale_exe, range_file, file_name, scaled_file)
        print('Scaling training data...')
        print(cmd)
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        #optimos con datos escalados
        cmd = '%s -svmtrain "%s" -gnuplot "%s" "%s"' % (grid_py, svmtrain_exe, gnuplot_exe,scaled_file)

        #obtener valores optimos sin datos escalados
        ###cmd = '%s -svmtrain "%s" -v 5 "%s"' % (grid_py, svmtrain_exe, file_name)

        print('Cross validation...')
        print(cmd)
        f = Popen(cmd, shell = True, stdout = PIPE).stdout

        line = ''
        while True:
            last_line = line
            line = f.readline()
            if not line: break
        c,g,rate = map(float,last_line.split())

        print('Best c=%s, g=%s CV rate=%s' % (c,g,rate))#### guardar BD  c = g =

        #entrenar con datos escalados
        cmd = '%s -c %s -g %s "%s" "%s"' % (svmtrain_exe,c,g,scaled_file,model_file)

        #entrenar sin datos escalados
        #cmd = '%s -c %s -g %s "%s" "%s"' % (svmtrain_exe,c,g,file_name,model_file)

        print('Training...')
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        print('Output model: %s' % model_file) # guardar BD
    except Exception, e:
        tamArgs=len(e.args)
        if tamArgs==0:
            errorDB= GenException("CreateFileFeatures: No info exception")
        if tamArgs==1:
            errorDB= GenException("CreateFileFeatures: %s" % (e.args[0]))
        if tamArgs==2:
            errorDB= GenException("CreateFileFeatures: %s: %s" % (e.args[0], e.args[1]))
        raise errorDB

def testSVM(self, PathClass = None, FileFeatTrain=None, fileTest=None,FileModel=None, FileRange=None):
    try:
        if(PathClass==None):
            PathClass = self.PathClass
        if(FileFeatTrain==None):
            FileFeatTrain = self.FileClass
        if(fileTest==None):
            fileTest = self.fileTest
        if(FileModel==None):
            FileModel = self.FileModel
        if(FileRange==None):
            FileRange = self.FileRange

        FileFeatTrain = os.path.join(PathClass, FileFeatTrain)
        fileTest = os.path.join(PathClass, fileTest)
        model_file = os.path.join(PathClass, FileModel)
        range_file = os.path.join(PathClass, FileRange)

        FileTestPredict = self.FileTestPredict
        FileTestScale = self.FileTestScale

        scaled_test_file = os.path.join(PathClass, FileTestScale)



        predict_test_file = os.path.join(PathClass, FileTestPredict)

        ##change current script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        #Definicion de ejecutables
        is_win32 = (sys.platform == 'win32')
        if not is_win32:
            svmscale_exe = "../LIBSVM/svm-scale"
            svmtrain_exe = "../LIBSVM/svm-train"
            svmpredict_exe = "../LIBSVM/svm-predict"
            grid_py = "../LIBSVM/grid.py"
            gnuplot_exe = "/usr/bin/gnuplot"
        else:
            #windows
            svmscale_exe = r"..\LIBSVM\svm-scale.exe"
            svmtrain_exe = r"..\LIBSVM\svm-train.exe"
            svmpredict_exe = r"..\LIBSVM\svm-predict.exe"
            grid_py = r"..\LIBSVM\grid.py"


        assert os.path.exists(svmscale_exe),"svm-scale executable not found"
        assert os.path.exists(svmtrain_exe),"svm-train executable not found"
        assert os.path.exists(svmpredict_exe),"svm-predict executable not found"
        assert os.path.exists(grid_py),"grid.py not found"

        #escalar datos
        cmd = '%s -r "%s" "%s" > "%s"' % (svmscale_exe, range_file, fileTest, scaled_test_file)
        print('Escalando datos de test...')
        print(cmd)
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        #test con datos escalados
        cmd = '%s "%s" "%s" "%s"' % (svmpredict_exe, scaled_test_file, model_file, predict_test_file)


        #test sin datos escalados
        #cmd = '%s "%s" "%s" "%s"' % (svmpredict_exe, fileTest, model_file, predict_test_file)
        print('Testeando...')
        print(cmd)
        Popen(cmd, shell = True).communicate()
        print('Salida prediccion: %s' % predict_test_file) # guardar bd
    except Exception, e:
        tamArgs=len(e.args)
        if tamArgs==0:
            errorDB= GenException("testSVM: No info exception")
        if tamArgs==1:
            errorDB= GenException("testSVM: %s" % (e.args[0]))
        if tamArgs==2:
            errorDB= GenException("testSVM: %s: %s" % (e.args[0], e.args[1]))
        raise errorDB

"""
def getFiles(self, nameDir, typeFile1, typeFile2=None):
    try:
        os.chdir(nameDir)
        typeFile1 = "*." + typeFile1
        lstFiles = glob.glob(typeFile1)
        if (typeFile2 != None):
            typeFile2 = "*." + typeFile2
            lstFiles.extend(glob.glob(typeFile2))
        return lstFiles
    except Exception, e:
        raise e

if __name__ == '__main__':
    sys.path.append("./ScannerVSCamera")

    #Opcion para obtener estadisticas que se guardan en un fichero, uso: mainSVM.py Folder outputFile mode
    #mode es un string de la forma "rcn" donde cada letra identifica el patron que queremos r=resize, c=cut y n=nothing ordenadas
    #las clases por orden alfabetico
    #
    if len(sys.argv) == 4:
        folder = sys.argv[1]
        out = sys.argv[2]
        mode = sys.argv[3]
        dirList=os.listdir(folder)
        dirList.sort()
        if(len(mode)==len(dirList)):
            i=0
            for fname in dirList:
                print fname
                if(mode[i]=="r"):
                    pass
                elif(mode[i]=="c"):
                    pass
                elif(mode[i]=="n"):
                    pass
                else: print "error: modo no reconocido, %s no se incluira",fname

                i=i+1
        else: print "error: longitud de modo diferente de numero de carpetas"


    #opcion para caracteristicas ya obtenidas, parametros
    if len(sys.argv) == 3:
        train_pathname = sys.argv[1]
        test_pathname=sys.argv[2]

        assert os.path.exists(train_pathname),"Archivo de entrenamiento no encontrado"
        assert os.path.exists(test_pathname),"Archivo de testeo no encontrado"

        model_pathname = train_pathname
        range_pathname = train_pathname

        print "Entrenando..."
        trainSVM(train_pathname)
        print 'Testeando...'
        testSVM(train_pathname,test_pathname,model_pathname, range_pathname)
    elif len(sys.argv) == 2:
        folderData = sys.argv[1]
        getFeaturesFromPath(_path=folderData)
        print "Entrenando..."
        trainSVM()
        print 'Testeando...'
        testSVM()
    elif len(sys.argv) == 1:
        print "Obteniendo Caracteristicas..."
        getFeaturesFromPathParallel()
        print ""
        os.chdir("E:\workspace\imgsource1\src")
        print "Entrenando..."
        trainSVM()
        print 'Testeando...'
        testSVM()
    else:
        print('Uso: python '+ sys.argv[0] + ' folderData'+ '/ python ' + sys.argv[0] + ' training_file testing_file')
        raise SystemExit

"""