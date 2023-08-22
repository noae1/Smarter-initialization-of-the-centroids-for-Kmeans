# define PY_SSIZE_T_CLEAN
# include <Python.h>       /* MUST include <Python.h>, this implies inclusion of the following standard headers:
                             <stdio.h>, <string.h>, <errno.h>, <limits.h>, <assert.h> and <stdlib.h> (if available). */
# include <math.h>         /* include <Python.h> has to be before any standard headers are included */
# include "cap.h"
PyObject* GetLisy_fromPyRes(int rows, int columns, double **data);

static PyObject* fit_capi(PyObject *self, PyObject *args)
{
    int i,j;
    PyObject *datalst;
    PyObject *centroidslst;
    int k;
    PyObject* res;
    double **rawres;
    int iter;
    double epsilon;
    int rowcount;
    int columncount;
    
    if(!PyArg_ParseTuple(args, "OOiifii", &centroidslst, &datalst, &k, &iter, &epsilon, &rowcount, &columncount)) {
        return NULL; 
    }
    double **data=malloc(rowcount*sizeof(double*)) ;
    if(data == NULL){
        printf("An Error Has Occurred");
        exit(1);
    }
    double **centroids=malloc(k*sizeof(double*)) ;
    if(centroids == NULL){
        printf("An Error Has Occurred");
        exit(1);
    }
    for (i=0;i<rowcount;i++){
        data[i] = malloc(columncount*sizeof(double));
        if(data[i] == NULL){
            printf("An Error Has Occurred");
            exit(1);
        }
        for (j=0;j<columncount;j++){
            data[i][j]= PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(datalst,i),j));
        }
    }
    for (i=0;i<k;i++){
        centroids[i] = malloc(columncount*sizeof(double));
        if(centroids[i] == NULL){
            printf("An Error Has Occurred");
            exit(1);
        }
        for (j=0;j<columncount;j++){
            centroids[i][j]= PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(centroidslst,i),j));
        }
    }
    //recompile 
    rawres = fit(centroids,data,k,iter,epsilon,rowcount,columncount); 
    res= GetLisy_fromPyRes(k,columncount,rawres);
     for (i=0;i<rowcount;i++){
        free(data[i]);
        
    }
    for (i=0;i<k;i++){
        free(rawres[i]);

        free(centroids[i]);
    }
    free(data);
    free(centroids);
    free(rawres);
    return res;
}

PyObject* GetLisy_fromPyRes(int rows, int columns, double **data)
{
    int i,j;
    PyObject* python_val;
    PyObject* inner_list;

    PyObject* python_double;
    python_val = PyList_New(rows);
    for (i = 0; i < rows; ++i)
    {
        inner_list=PyList_New(columns);
        for(j = 0; j<columns;j++){
            python_double = Py_BuildValue("d", data[i][j]);
            PyList_SetItem(inner_list, j, python_double);
        }
        PyList_SetItem(python_val, i, inner_list);

    }
    return python_val;
}
static PyMethodDef capiMethods[] = {
    {"fit",                   
      (PyCFunction) fit_capi, 
      METH_VARARGS,         
      PyDoc_STR("Kmeans algorithm from HW1.getting initial centroids, data,k, max iteration number, trashjold epsilon value, data rows count  and data column count")}, 
    {NULL, NULL, 0, NULL}     
};


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", 
    NULL, 
    -1,  
    capiMethods 
};

PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}