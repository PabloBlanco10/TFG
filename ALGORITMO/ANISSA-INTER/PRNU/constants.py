# constants.py
DEFAULT_PATH = "."
CROPPED_PREFIX = "cropped_"
DENOISED_PREFIX = "denoised_"
NOISE_PREFIX = "noise_"
FEATURES_PREFIX = "features"
PROM_NOISE_NAME = "prom_noise.jpg"
ZERO_MEAN_SUFFIX = "_ConMean"
NOZERO_MEAN_SUFFIX = "_SinMean"
N3_SUFFIX = "_N3"
N3579_SUFFIX = "_N3579"
EXTS = ['.jpg', '.jpeg', '.JPG']

WAVELET = "db8" #db4 daubechies 4-tab, db8 daubechies 8-tab, haar haar
LEVEL = 4       # descomposition level
MODE = "sym"    # getting edge artifacts
SIGMA = 0.707106781186548

FEATURES_REQUIRED = True

TRAIN_CLASS_ID = "1 "
CROP_REQUIRED = True
CROP_X_SIZE = 1024
CROP_Y_SIZE = 1024
ZEROMEAN_REQUIRED = False #Optimizar calidad de la huella extraida
MULTIPLE_NEIGHBOR = False #Calculo de variancia con distintos tamanio de ventana 3-5-7-9

CROPCENT_REQUIRED = True #Si se requiere la ROI del centro de lo contrario es la esquina superior izq
SAVEIMGS_REQUIRED = False
AUGGREEN_REQUIRED = True

# argumentos para la extraccion de caracteristicas de video # Carlos

VIDEO_EXTS = ['.3gp', '.mov', '.mp4']
EXTRACTION_METHOD= "histogram" # histogram|partition|all
NUMBER_OF_FRAMES = 10
INIT_THRESHOLD = -0.27
STEP_THRESHOLD = 0.0001
FILE_PATTERN="frame_%d.jpg"

#Daton ...
# tamanio bloque ruidos
TAM_BLOQUE_RUIDO=128
#constante k para preclasificador  de detector de falsificaciones
##presupongo que es natural
K_PRE=2
##constante para definir umbral de bloques erroneos, para que un fotograma se considere anomalo
Q_DET=0