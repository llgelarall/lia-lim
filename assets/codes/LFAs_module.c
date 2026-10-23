#include <Python.h>

// Include the LFAs.c code
#include "LFAs.c"

// Define the Python wrapper for the py_unsgn_LFA_21_21_MAE_PE_Best
static PyObject* py_unsgn_LFA_21_21_MAE_PE_Best(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_MAE_PE_Best function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_MAE_PE_Best(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the Python wrapper for the py_unsgn_LFA_21_21_MSE_Best
static PyObject* py_unsgn_LFA_21_21_MSE_Best(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_MSE_Best function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_MSE_Best(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the Python wrapper for the unsgn_LFA_21_21_MSE_Best_2 function
static PyObject* py_unsgn_LFA_21_21_MSE_Best_2(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_MSE_Best_2 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_MSE_Best_2(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the Python wrapper for the unsgn_LFA_21_21_ME_N25_LOA function
static PyObject* py_unsgn_LFA_21_21_ME_N25_LOA(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N25_LOA function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N25_LOA(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the Python wrapper for the unsgn_LFA_21_21_ME_Best function
static PyObject* py_unsgn_LFA_21_21_ME_Best(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_Best function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_Best(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the Python wrapper for the unsgn_LFA_21_21_ME_N50_1 function
static PyObject* py_unsgn_LFA_21_21_ME_N50_1(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N50_1 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N50_1(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_0_1(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the py_unsgn_LFA_21_21_ME_0_1 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_0_1(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_0_2(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_0_2 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_0_2(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_P25(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_P25 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_P25(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_N25_2(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N25_2 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N25_2(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_N25_3(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N25_3 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N25_3(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_N25_4(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N25_4 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N25_4(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_P50(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_P50 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_P50(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

static PyObject* py_unsgn_LFA_21_21_ME_N50_2(PyObject* self, PyObject* args) {
    unsigned long int input1, input2;
    unsigned int input_length, lower_part_length;

    // Parse the function arguments from Python
    if (!PyArg_ParseTuple(args, "KKII", &input1, &input2, &input_length, &lower_part_length)) {
        return NULL;
    }

    // Call the unsgn_LFA_21_21_ME_N50_2 function from LFAs.c
    unsigned int result = unsgn_LFA_21_21_ME_N50_2(input1, input2, input_length, lower_part_length);

    // Return the result as a Python integer
    return Py_BuildValue("I", result);
}

// Define the module's method table
static PyMethodDef LFAs_module_methods[] = {
    {"unsgn_LFA_21_21_MAE_PE_Best", py_unsgn_LFA_21_21_MAE_PE_Best, METH_VARARGS, "Perform unsgn_LFA_21_21_MAE_PE_Best operation."},
    {"unsgn_LFA_21_21_MSE_Best", py_unsgn_LFA_21_21_MSE_Best, METH_VARARGS, "Perform unsgn_LFA_21_21_MSE_Best operation."},
    {"unsgn_LFA_21_21_MSE_Best_2", py_unsgn_LFA_21_21_MSE_Best_2, METH_VARARGS, "Perform unsgn_LFA_21_21_MSE_Best_2 operation."},
    {"unsgn_LFA_21_21_ME_N25_LOA", py_unsgn_LFA_21_21_ME_N25_LOA, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N25_LOA operation."},
    {"unsgn_LFA_21_21_ME_N50_1", py_unsgn_LFA_21_21_ME_N50_1, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N50_1 operation."},
    {"unsgn_LFA_21_21_ME_Best", py_unsgn_LFA_21_21_ME_Best, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_Best operation."},
    {"unsgn_LFA_21_21_ME_0_1", py_unsgn_LFA_21_21_ME_0_1, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_0_1 operation."},
    {"unsgn_LFA_21_21_ME_0_2", py_unsgn_LFA_21_21_ME_0_2, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_0_2 operation."},
    {"unsgn_LFA_21_21_ME_P25", py_unsgn_LFA_21_21_ME_P25, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_P25 operation."},
    {"unsgn_LFA_21_21_ME_N25_2", py_unsgn_LFA_21_21_ME_N25_2, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N25_2 operation."},
    {"unsgn_LFA_21_21_ME_N25_3", py_unsgn_LFA_21_21_ME_N25_3, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N25_3 operation."},
    {"unsgn_LFA_21_21_ME_N25_4", py_unsgn_LFA_21_21_ME_N25_4, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N25_4 operation."},
    {"unsgn_LFA_21_21_ME_P50", py_unsgn_LFA_21_21_ME_P50, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_P50 operation."},
    {"unsgn_LFA_21_21_ME_N50_2", py_unsgn_LFA_21_21_ME_N50_2, METH_VARARGS, "Perform unsgn_LFA_21_21_ME_N50_2 operation."},
    {NULL, NULL, 0, NULL}
};

// Define the module initialization function
static struct PyModuleDef LFAs_module_definition = {
    PyModuleDef_HEAD_INIT,
    "LFAs_module",
    "A Python extension module for LFAs",
    -1,
    LFAs_module_methods
};

PyMODINIT_FUNC PyInit_LFAs_module(void) {
    return PyModule_Create(&LFAs_module_definition);
}
