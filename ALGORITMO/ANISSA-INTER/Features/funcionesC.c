#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>

static PyObject *funcionesC_gauss(PyObject *self,PyObject *args){
	 PyObject *imObject,*nucObject,*resObject;
	 PyArrayObject *imagen,*nucleo,*resultado;
	 PyArg_ParseTuple(args,"OOO", &imObject, &nucObject, &resObject);
	 imagen = (PyArrayObject *)imObject;
	 nucleo = (PyArrayObject *)nucObject;
	 resultado = (PyArrayObject *)resObject;
	 int alto = PyArray_DIMS(imagen)[1];
	 int ancho = PyArray_DIMS(imagen)[2];
	 int i,j;
	 double n00,n01,n02,n10,n11,n12,n20,n21,n22;
	 n00 = *(double*)PyArray_GETPTR2(nucleo,0,0);
	 n01 = *(double*)PyArray_GETPTR2(nucleo,0,1);
	 n02 = *(double*)PyArray_GETPTR2(nucleo,0,2);
	 n10 = *(double*)PyArray_GETPTR2(nucleo,1,0);
	 n11 = *(double*)PyArray_GETPTR2(nucleo,1,1);
	 n12 = *(double*)PyArray_GETPTR2(nucleo,1,2);
	 n20 = *(double*)PyArray_GETPTR2(nucleo,2,0);
	 n21 = *(double*)PyArray_GETPTR2(nucleo,2,1);
	 n22 = *(double*)PyArray_GETPTR2(nucleo,2,2);
	 
	 for(i=0;i<alto;i++){
		for(j=0;j<ancho;j++){
			//Caso general
            if (i>0 && i<alto-1 && j>0 && j<ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j+1))*n22);		
			}
			//Tratamiento de la fila superior 
            else if (i==0 && j>0 && j<ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j+1))*n22);
			}
			//Tratamiento de la fila inferior 
            else if (i==alto-1 && j>0 && j<ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12);
			}
			//Tratamiento de la columna izquierda 
            else if (i>0 && i<alto-1 && j==0){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j+1))*n22);
			}
			//Tratamiento de la columna derecha 
            else if (i>0 && i<alto-1 && j==ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21);
			}
			//Tratamiento de la esquina superior izquierda
            else if (i==0 && j==0){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j+1))*n22);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j+1))*n22);
			}
			//Tratamiento de la esquina superior derecha
            else if (i==0 && j==ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i+1,j))*n21);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i+1,j))*n21);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j-1))*n20 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i+1,j))*n21);
			}
			//Tratamiento de la esquina inferior izquierda
            else if (i==alto-1 && j==0){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j+1))*n12);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j+1))*n12);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j+1))*n02 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j+1))*n12);
			}
			//Tratamiento de la esquina inferior derecha
            else if (i==alto-1 && j==ancho-1){
				*(unsigned char*)PyArray_GETPTR3(resultado,0,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j))*n11);
				*(unsigned char*)PyArray_GETPTR3(resultado,1,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j))*n11);
				*(unsigned char*)PyArray_GETPTR3(resultado,2,i,j) = (unsigned char)((*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j-1))*n00 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i-1,j))*n01 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j-1))*n10 + (*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j))*n11);
			}
		}
	 }
	

	 return Py_BuildValue("i",0);
}

static PyObject *funcionesC_czekonowskyDistance(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j,k,num,den;
	float suma=0;
	unsigned char cO, cS; 
	for(i=0;i<alto;i++){
		for(j=0;j<ancho;j++){
			num = 0;
			den = 0;
			for(k=0;k<3;k++){
				cO = (*(unsigned char*)PyArray_GETPTR3(imagenO,k,i,j));
				cS = (*(unsigned char*)PyArray_GETPTR3(imagenS,k,i,j));
				if(cO<cS)
					num = num + cO;
				else
					num = num + cS;
				den = den + cO + cS;
				}
			
			if(den!=0)
				suma = suma + (1 - (2*num/(float)den)); //importante hacer casting a float
		}
	}
	float res = suma/(ancho*alto);
	return Py_BuildValue("f",res);
}

static PyObject *funcionesC_minkowskyMetric(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	int gamma;
	PyArg_ParseTuple(args,"OOi", &imOObject, &imSObject, &gamma);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double sumaR=0, sumaG=0, sumaB=0;
	if(gamma==1){
		for(i=0;i<alto;i++){                               
			for(j=0;j<ancho;j++){
				sumaR = sumaR + fabs((*(unsigned char*)PyArray_GETPTR3(imagenO,0,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,0,i,j)));
				sumaG = sumaG + fabs((*(unsigned char*)PyArray_GETPTR3(imagenO,1,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,1,i,j)));
				sumaB = sumaB + fabs((*(unsigned char*)PyArray_GETPTR3(imagenO,2,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,2,i,j)));
			}
		}
	}
	if(gamma==2){
		for(i=0;i<alto;i++){                                
			for(j=0;j<ancho;j++){
				sumaR = sumaR + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,0,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,0,i,j)),2);
				sumaG = sumaG + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,1,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,1,i,j)),2);
				sumaB = sumaB + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,2,i,j))-(*(unsigned char*)PyArray_GETPTR3(imagenS,2,i,j)),2);
			}
		}
	}
	
	double mmR = sumaR/(alto*ancho);
	double mmG = sumaG/(alto*ancho);
	double mmB = sumaB/(alto*ancho);
	
	return Py_BuildValue("ddd",mmR,mmG,mmB);
}

static PyObject *funcionesC_structuralContent(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double sumRO=0, sumGO=0, sumBO=0, sumRS=0, sumGS=0, sumBS=0;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			sumRO = sumRO + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,0,i,j)),2);
			sumGO = sumGO + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,1,i,j)),2);
			sumBO = sumBO + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,2,i,j)),2);
			sumRS = sumRS + pow((*(unsigned char*)PyArray_GETPTR3(imagenS,0,i,j)),2);
			sumGS = sumGS + pow((*(unsigned char*)PyArray_GETPTR3(imagenS,1,i,j)),2);
			sumBS = sumBS + pow((*(unsigned char*)PyArray_GETPTR3(imagenS,2,i,j)),2);
		}
	}	
	double scR = sumRO / sumRS;
	double scG = sumGO / sumGS;
	double scB = sumBO / sumBS;
	
	return Py_BuildValue("ddd",scR,scG,scB);
}
	
	
static PyObject *funcionesC_normalizedCrossCorrelation(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double numR=0, numG=0, numB=0, denR=0, denG=0, denB=0;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			numR = numR + ((*(unsigned char*)PyArray_GETPTR3(imagenO,0,i,j))*(*(unsigned char*)PyArray_GETPTR3(imagenS,0,i,j)));
			numG = numG + ((*(unsigned char*)PyArray_GETPTR3(imagenO,1,i,j))*(*(unsigned char*)PyArray_GETPTR3(imagenS,1,i,j)));
			numB = numB + ((*(unsigned char*)PyArray_GETPTR3(imagenO,2,i,j))*(*(unsigned char*)PyArray_GETPTR3(imagenS,2,i,j)));
			denR = denR + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,0,i,j)),2);
			denG = denG + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,1,i,j)),2);
			denB = denB + pow((*(unsigned char*)PyArray_GETPTR3(imagenO,2,i,j)),2);
		}
	}
	
	double nccR = numR / denR;
    double nccG = numG / denG;
    double nccB = numB / denB;

	return Py_BuildValue("ddd",nccR,nccG,nccB);
}

int operadorLaplaciano(PyArrayObject *matriz, int k, int x, int y){
	int res;
	res = (*(unsigned char*)PyArray_GETPTR3(matriz,k,x+1,y)) + (*(unsigned char*)PyArray_GETPTR3(matriz,k,x-1,y)) + (*(unsigned char*)PyArray_GETPTR3(matriz,k,x,y+1)) + (*(unsigned char*)PyArray_GETPTR3(matriz,k,x,y-1)) + 4*(*(unsigned char*)PyArray_GETPTR3(matriz,k,x,y));
	return res;
}

static PyObject *funcionesC_laplacianMeanSquareError(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double numR=0, numG=0, numB=0, denR=0, denG=0, denB=0;
	int opR,opG,opB;
	for(i=1;i<alto-1;i++){                                
		for(j=1;j<ancho-1;j++){
			opR = operadorLaplaciano(imagenO,0,i,j);
			opG = operadorLaplaciano(imagenO,1,i,j);
			opB = operadorLaplaciano(imagenO,2,i,j);
			numR = numR + pow(opR-operadorLaplaciano(imagenS,0,i,j),2);
			numG = numG + pow(opG-operadorLaplaciano(imagenS,1,i,j),2);
			numB = numB + pow(opB-operadorLaplaciano(imagenS,2,i,j),2);
			denR = denR + pow(opR,2);
			denG = denG + pow(opG,2);
			denB = denB + pow(opB,2);
		}
	}
		
	double lmseR = numR / denR;
	double lmseG = numG / denG;
	double lmseB = numB / denB;
		
	return Py_BuildValue("ddd",lmseR,lmseG,lmseB);	
}	
/*	
static PyObject *funcionesC_neighborDistribution(PyObject *self,PyObject *args){
	PyObject *imObject,*imResR,*imResG,*imResB;
	PyArrayObject *imagen,*resR,*resG,*resB;
	PyArg_ParseTuple(args,"OOOO", &imObject, &imResR, &imResG, &imResB);
	imagen = (PyArrayObject *)imObject;
	resR = (PyArrayObject *)imResR;
	resG = (PyArrayObject *)imResG;
	resB = (PyArrayObject *)imResB;
	int alto = PyArray_DIMS(imagen)[1];
	int ancho = PyArray_DIMS(imagen)[2];
	int i,j,k,l,fil,col;
	unsigned char neighborsR, neighborsG, neighborsB;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			neighborsR=0; neighborsG=0; neighborsB=0;
			for(k=-1;k<2;k++){                                
				for(l=-1;l<2;l++){
					fil = i+k;
					col = j+l;
					if(k!=0 && l!=0){
						if(fil>=0 && fil<alto && col>=0 && col<ancho){
							if(fabs(*(unsigned char*)PyArray_GETPTR3(imagen,0,i,j)-*(unsigned char*)PyArray_GETPTR3(imagen,0,fil,col))==1)
								neighborsR = neighborsR + 1;
							if(fabs(*(unsigned char*)PyArray_GETPTR3(imagen,1,i,j)-*(unsigned char*)PyArray_GETPTR3(imagen,1,fil,col))==1)
								neighborsG = neighborsG + 1;
							if(fabs(*(unsigned char*)PyArray_GETPTR3(imagen,2,i,j)-*(unsigned char*)PyArray_GETPTR3(imagen,2,fil,col))==1)
								neighborsB = neighborsB + 1;
						}
					}
				}
			}
			*(unsigned char*)PyArray_GETPTR2(resR,i,j) = neighborsR;
			*(unsigned char*)PyArray_GETPTR2(resG,i,j) = neighborsG;
			*(unsigned char*)PyArray_GETPTR2(resB,i,j) = neighborsB;
		}
	}

	return Py_BuildValue("i",0);
}	*/

static PyObject *funcionesC_neighborDistribution(PyObject *self,PyObject *args){

	PyObject *imObject, *neigObject;
	PyArrayObject *imagen, *neighbors;
	PyArg_ParseTuple(args,"OO", &imObject, &neigObject);
	imagen = (PyArrayObject *)imObject;
	neighbors = (PyArrayObject *)neigObject;
	int alto = PyArray_DIMS(imagen)[0];
	int ancho = PyArray_DIMS(imagen)[1];
	int i,j;
	int numPixeles[256];
	
	//int sumNeighbors;
	
	for(i=0;i<256;i++)                                
		numPixeles[i] = 0;
		
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			numPixeles[*(unsigned char*)PyArray_GETPTR2(imagen,i,j)] = numPixeles[*(unsigned char*)PyArray_GETPTR2(imagen,i,j)] + 1;
		}
	}
	
	*(int*)PyArray_GETPTR1(neighbors,0) = numPixeles[1];
	for(i=1;i<255;i++)
		*(int*)PyArray_GETPTR1(neighbors,i) = numPixeles[i-1] + numPixeles[i+1];
	*(int*)PyArray_GETPTR1(neighbors,255) = numPixeles[254];
		
	return Py_BuildValue("i",0);
}	


double bandPassFilter(double p){
	if(p<7)
		return 0.05*(pow(exp(1),pow(p,0.554)));
	else
		return pow(exp(1),-9*pow(fabs(log10(p)-log10(9)),2.3));
}	

static PyObject *funcionesC_bucle1HVS(PyObject *self,PyObject *args){
	PyObject *uRObject,*uGObject,*uBObject,*uR2Object,*uG2Object,*uB2Object;
	PyArrayObject *uR,*uG,*uB,*uR2,*uG2,*uB2;
	PyArg_ParseTuple(args,"OOOOOO", &uRObject, &uGObject, &uBObject, &uR2Object, &uG2Object, &uB2Object);
	uR = (PyArrayObject *)uRObject;
	uG = (PyArrayObject *)uGObject;
	uB = (PyArrayObject *)uBObject;
	uR2 = (PyArrayObject *)uR2Object;
	uG2 = (PyArrayObject *)uG2Object;
	uB2 = (PyArrayObject *)uB2Object;
	int alto = PyArray_DIMS(uR)[0];
	int ancho = PyArray_DIMS(uR)[1];
	int i,j;
	double H;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			H = bandPassFilter(pow((pow(i,2)+pow(j,2)),0.5));
			*(double*)PyArray_GETPTR2(uR,i,j) = *(double*)PyArray_GETPTR2(uR,i,j) * H;
			*(double*)PyArray_GETPTR2(uG,i,j) = *(double*)PyArray_GETPTR2(uG,i,j) * H;
			*(double*)PyArray_GETPTR2(uB,i,j) = *(double*)PyArray_GETPTR2(uB,i,j) * H;
			*(double*)PyArray_GETPTR2(uR2,i,j) = *(double*)PyArray_GETPTR2(uR2,i,j) * H;
			*(double*)PyArray_GETPTR2(uG2,i,j) = *(double*)PyArray_GETPTR2(uG2,i,j) * H;
			*(double*)PyArray_GETPTR2(uB2,i,j) = *(double*)PyArray_GETPTR2(uB2,i,j) * H;
		}
	}
			
	return Py_BuildValue("i",0);	
}	

static PyObject *funcionesC_bucle2HVS(PyObject *self,PyObject *args){
	PyObject *uRObject,*uGObject,*uBObject,*uR2Object,*uG2Object,*uB2Object;
	PyArrayObject *uR,*uG,*uB,*uR2,*uG2,*uB2;
	PyArg_ParseTuple(args,"OOOOOO", &uRObject, &uGObject, &uBObject, &uR2Object, &uG2Object, &uB2Object);
	uR = (PyArrayObject *)uRObject;
	uG = (PyArrayObject *)uGObject;
	uB = (PyArrayObject *)uBObject;
	uR2 = (PyArrayObject *)uR2Object;
	uG2 = (PyArrayObject *)uG2Object;
	uB2 = (PyArrayObject *)uB2Object;
	int alto = PyArray_DIMS(uR)[0];
	int ancho = PyArray_DIMS(uR)[1];
	int i,j;
	double numNAER=0, numNAEG=0, numNAEB=0, denNAER=0, denNAEG=0, denNAEB=0, sumL2R=0, sumL2G=0, sumL2B=0;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			numNAER = numNAER + fabs(*(double*)PyArray_GETPTR2(uR,i,j)-*(double*)PyArray_GETPTR2(uR2,i,j));
			numNAEG = numNAEG + fabs(*(double*)PyArray_GETPTR2(uG,i,j)-*(double*)PyArray_GETPTR2(uG2,i,j));
			numNAEB = numNAEB + fabs(*(double*)PyArray_GETPTR2(uB,i,j)-*(double*)PyArray_GETPTR2(uB2,i,j));
			denNAER = denNAER + fabs(*(double*)PyArray_GETPTR2(uR,i,j));
			denNAEG = denNAEG + fabs(*(double*)PyArray_GETPTR2(uG,i,j));
			denNAEB = denNAEB + fabs(*(double*)PyArray_GETPTR2(uB,i,j));
			sumL2R = sumL2R + pow(fabs(*(double*)PyArray_GETPTR2(uR,i,j)-*(double*)PyArray_GETPTR2(uR2,i,j)),2);
			sumL2G = sumL2G + pow(fabs(*(double*)PyArray_GETPTR2(uG,i,j)-*(double*)PyArray_GETPTR2(uG2,i,j)),2);
			sumL2B = sumL2B + pow(fabs(*(double*)PyArray_GETPTR2(uB,i,j)-*(double*)PyArray_GETPTR2(uB2,i,j)),2);
		}
	}
	
	//Normalized Absolute Error (HVS)        
	double NAER = numNAER/denNAER;
	double NAEG = numNAEG/denNAEG;
	double NAEB = numNAEB/denNAEB;
	//HVS Based L2
	double L2R = pow((sumL2R/(alto*ancho)),0.5);
	double L2G = pow((sumL2G/(alto*ancho)),0.5);
	double L2B = pow((sumL2B/(alto*ancho)),0.5);
	
	return Py_BuildValue("dddddd",NAER,NAEG,NAEB,L2R,L2G,L2B);	
}	

double absComplex(Py_complex *c){
	return sqrt(pow(c->real,2) + pow(c->imag,2));
} 

static PyObject *funcionesC_spectralPhase(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double sumR=0, sumG=0, sumB=0;
	double psOR,psOG,psOB,psSR,psSG,psSB;
	Py_complex *p1,*p2,*p3,*p4,*p5,*p6;
	double abs1,abs2,abs3;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			p1 = (Py_complex*)PyArray_GETPTR3(imagenO,0,i,j);
			p2 = (Py_complex*)PyArray_GETPTR3(imagenO,1,i,j);
			p3 = (Py_complex*)PyArray_GETPTR3(imagenO,2,i,j);
			p4 = (Py_complex*)PyArray_GETPTR3(imagenS,0,i,j);
			p5 = (Py_complex*)PyArray_GETPTR3(imagenS,1,i,j);
			p6 = (Py_complex*)PyArray_GETPTR3(imagenS,2,i,j);
			psOR = atan2(p1->imag, p1->real);
			psOG = atan2(p2->imag, p2->real);
			psOB = atan2(p3->imag, p3->real);	
			psSR = atan2(p4->imag, p4->real);
			psSG = atan2(p5->imag, p5->real);
			psSB = atan2(p6->imag, p6->real);
			abs1 = fabs(psOR - psSR);
			abs2 = fabs(psOG - psSG);
			abs3 = fabs(psOB - psSB);
			sumR = sumR + abs1*abs1;
			sumG = sumG + abs2*abs2;
			sumB = sumB + abs3*abs3;
		}
	}
		
	double spR = sumR / (alto*ancho);
	double spG = sumG / (alto*ancho);
	double spB = sumB / (alto*ancho);
		
	return Py_BuildValue("ddd",spR,spG,spB);	
		
}

static PyObject *funcionesC_spectralMagnitude(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	PyArg_ParseTuple(args,"OO", &imOObject, &imSObject);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	double sumR=0, sumG=0, sumB=0;
	double msOR,msOG,msOB,msSR,msSG,msSB;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			msOR = absComplex((Py_complex*)PyArray_GETPTR3(imagenO,0,i,j));
			msOG = absComplex((Py_complex*)PyArray_GETPTR3(imagenO,1,i,j));
			msOB = absComplex((Py_complex*)PyArray_GETPTR3(imagenO,2,i,j));	
			msSR = absComplex((Py_complex*)PyArray_GETPTR3(imagenS,0,i,j));
			msSG = absComplex((Py_complex*)PyArray_GETPTR3(imagenS,1,i,j));
			msSB = absComplex((Py_complex*)PyArray_GETPTR3(imagenS,2,i,j));
			sumR = sumR + pow(fabs(msOR - msSR),2);
			sumG = sumG + pow(fabs(msOG - msSG),2);
			sumB = sumB + pow(fabs(msOB - msSB),2);
		}
	}
		
	double smR = sumR / (alto*ancho);
	double smG = sumG / (alto*ancho);
	double smB = sumB / (alto*ancho);
		
	return Py_BuildValue("ddd",smR,smG,smB);	
		
}

static PyObject *funcionesC_siguienteBloque(PyObject *self,PyObject *args){
	int posX, posY, sizeImX, sizeImY, blockSize;
	PyArg_ParseTuple(args,"iiiii", &posX, &posY, &sizeImX, &sizeImY, &blockSize);
	
	//determino la esquina inferior derecha del bloque actual
	int resX, resY, nextX, nextY;
	if((posX+blockSize-1)<=sizeImX)
		resX = posX+blockSize-1;
	else
		resX = sizeImX-1;
	if((posY+blockSize-1)<=sizeImY)
		resY = posY+blockSize-1;
	else
		resY = sizeImY-1;
	//determino el comienzo del siguiente bloque    
	if(resX==sizeImX-1){
		nextX = 0;
		nextY = resY + 1;
	}
	else{
		nextX = resX + 1;
		nextY = posY;
	}
	
	return Py_BuildValue("iiii",resX, resY, nextX, nextY);		
}

static PyObject *funcionesC_bucleMBF(PyObject *self,PyObject *args){
	PyObject *imOObject,*imSObject;
	PyArrayObject *imagenO,*imagenS;
	double gamma, lambd;
	PyArg_ParseTuple(args,"OOdd", &imOObject, &imSObject, &gamma, &lambd);
	imagenO = (PyArrayObject *)imOObject;
	imagenS = (PyArrayObject *)imSObject;
	int alto = PyArray_DIMS(imagenO)[1];
	int ancho = PyArray_DIMS(imagenO)[2];
	int i,j;
	Py_complex *OR,*OG,*OB,*SR,*SG,*SB;
	double sumR=0, sumG=0, sumB=0, sumR2=0, sumG2=0, sumB2=0, sumR3=0, sumG3=0, sumB3=0;
	double msOR,msOG,msOB,msSR,msSG,msSB;
	double psOR,psOG,psOB,psSR,psSG,psSB;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			OR = (Py_complex*)PyArray_GETPTR3(imagenO,0,i,j);
			OG = (Py_complex*)PyArray_GETPTR3(imagenO,1,i,j);
			OB = (Py_complex*)PyArray_GETPTR3(imagenO,2,i,j);	
			SR = (Py_complex*)PyArray_GETPTR3(imagenS,0,i,j);
			SG = (Py_complex*)PyArray_GETPTR3(imagenS,1,i,j);
			SB = (Py_complex*)PyArray_GETPTR3(imagenS,2,i,j);
			msOR = absComplex(OR);
			msOG = absComplex(OG);
			msOB = absComplex(OB);
			msSR = absComplex(SR);
			msSG = absComplex(SG);
			msSB = absComplex(SB);
			psOR = atan2(OR->imag, OR->real);
			psOG = atan2(OG->imag, OG->real);
			psOB = atan2(OB->imag, OB->real);	
			psSR = atan2(SR->imag, SR->real);
			psSG = atan2(SG->imag, SG->real);
			psSB = atan2(SB->imag, SB->real);
			
			sumR = sumR + pow(fabs(msOR - msSR),gamma);
			sumG = sumG + pow(fabs(msOG - msSG),gamma);
			sumB = sumB + pow(fabs(msOB - msSB),gamma);
			sumR2 = sumR2 + pow(fabs(psOR - psSR),gamma);
			sumG2 = sumG2 + pow(fabs(psOG - psSG),gamma);
			sumB2 = sumB2 + pow(fabs(psOB - psSB),gamma);
		}
	}
	
	sumR = pow(sumR,(1.0/gamma));
	sumG = pow(sumG,(1.0/gamma));
	sumB = pow(sumB,(1.0/gamma));
	sumR2 = pow(sumR2,(1.0/gamma));
	sumG2 = pow(sumG2,(1.0/gamma));
	sumB2 = pow(sumB2,(1.0/gamma));
	sumR3 = lambd*sumR + (1-lambd)*sumR2;
	sumG3 = lambd*sumG + (1-lambd)*sumG2;
	sumB3 = lambd*sumB + (1-lambd)*sumB2;
		
	return Py_BuildValue("ddddddddd",sumR, sumG, sumB, sumR2, sumG2, sumB2, sumR3, sumG3, sumB3);	
		
}

double desviacionTipica(PyArrayObject* matriz){
	int alto = PyArray_DIMS(matriz)[0];
	int ancho = PyArray_DIMS(matriz)[1];
	double suma = 0;
	int i,j;
	//Hallo la media de las componentes de la matriz
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			suma = suma + *(unsigned char*)PyArray_GETPTR2(matriz,i,j);
		}
	}
	double media = suma / (ancho*alto);
	//Calculo la desviacion tipica
	suma = 0;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			suma = suma + pow((*(unsigned char*)PyArray_GETPTR2(matriz,i,j) - media),2);
		}
	}
	return pow((suma/(ancho*alto - 1)),0.5);
}

double covarianza(PyArrayObject* matriz1, PyArrayObject* matriz2){
	//Las dos matrices deben tener el mismo tamanio
	int alto = PyArray_DIMS(matriz1)[0];
	int ancho = PyArray_DIMS(matriz1)[1];
	//Hallo la media de las componentes de la matrices
	double suma1 = 0;
    double suma2 = 0;
	int i,j;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			suma1 = suma1 + *(unsigned char*)PyArray_GETPTR2(matriz1,i,j);
			suma2 = suma2 + *(unsigned char*)PyArray_GETPTR2(matriz2,i,j);
		}
	}
	double media1 = suma1 / (ancho*alto);
    double media2 = suma2 / (ancho*alto);
	//Calculo la covarianza
	double suma = 0;
	for(i=0;i<alto;i++){                                
		for(j=0;j<ancho;j++){
			suma = suma + (*(unsigned char*)PyArray_GETPTR2(matriz1,i,j)-media1)*(*(unsigned char*)PyArray_GETPTR2(matriz2,i,j)-media2);
		}
	}
	return suma/(ancho*alto);
}

static PyObject *funcionesC_pearson(PyObject *self,PyObject *args){
	PyObject *imObject1,*imObject2;
	PyArrayObject *matriz1,*matriz2;
	PyArg_ParseTuple(args,"OO", &imObject1, &imObject2);
	matriz1 = (PyArrayObject *)imObject1;
	matriz2 = (PyArrayObject *)imObject2;

	double res = covarianza(matriz1, matriz2)/(desviacionTipica(matriz1)*desviacionTipica(matriz2));

    return Py_BuildValue("d",res);	
}

/*
static PyObject *funcionesC_liberarArray(PyObject *self,PyObject *args){
	PyObject *imObject1;
	//PyArrayObject *matriz1;
	PyArg_ParseTuple(args,"O", &imObject1);
	//matriz1 = (PyArrayObject *)imObject1;
	
	Py_DECREF(imObject1);
	free(imObject1);
	

    return Py_BuildValue("i",0);	
}*/

static PyMethodDef funcionesCMethods[] = {
 {"gauss", funcionesC_gauss, METH_VARARGS, "Bucle del filtro gaussiano"},
 {"czekonowskyDistance", funcionesC_czekonowskyDistance, METH_VARARGS, "Distancia czekonowsky"},
 {"minkowskyMetric", funcionesC_minkowskyMetric, METH_VARARGS, "Minkowsky Metric"},
 {"structuralContent", funcionesC_structuralContent, METH_VARARGS, "Structural Content"},
 {"normalizedCrossCorrelation", funcionesC_normalizedCrossCorrelation, METH_VARARGS, "Normalized Cross Correlation"},
 {"laplacianMeanSquareError", funcionesC_laplacianMeanSquareError, METH_VARARGS, "Laplacian Mean Square Error"},
 {"neighborDistribution", funcionesC_neighborDistribution, METH_VARARGS, "Neighbor Distribution"},
 {"bucle1HVS", funcionesC_bucle1HVS, METH_VARARGS, "Bucle 1 para las HVS features"},
 {"bucle2HVS", funcionesC_bucle2HVS, METH_VARARGS, "Bucle 2 para las HVS features"},
 {"spectralPhase", funcionesC_spectralPhase, METH_VARARGS, "Spectral Phase"},
 {"spectralMagnitude", funcionesC_spectralMagnitude, METH_VARARGS, "Spectral Magnitude"},
 {"siguienteBloque", funcionesC_siguienteBloque, METH_VARARGS, "Siguiente Bloque"},
 {"bucleMBF", funcionesC_bucleMBF, METH_VARARGS, "Bucle Median Block Features"},
 {"pearson", funcionesC_pearson, METH_VARARGS, "Pearson"},
 {NULL, NULL, 0, NULL}
 };

 void initfuncionesC(void){
 (void) Py_InitModule("funcionesC", funcionesCMethods);
 }
